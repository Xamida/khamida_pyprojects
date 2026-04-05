(function ($) {
    "use strict";

    /* Range Two Price
    -------------------------------------------------------------------------*/
    var rangeTwoPrice = function () {
        if ($("#price-value-range").length > 0) {
            var skipSlider = document.getElementById("price-value-range");
            var skipValues = [document.getElementById("price-min-value"), document.getElementById("price-max-value")];

            var min = parseInt(skipSlider.getAttribute("data-min")) || 0;
            var max = parseInt(skipSlider.getAttribute("data-max")) || 500;

            noUiSlider.create(skipSlider, {
                start: [min, max],
                connect: true,
                step: 1,
                range: {
                    min: min,
                    max: max,
                },
                format: {
                    from: function (value) {
                        return parseInt(value);
                    },
                    to: function (value) {
                        return parseInt(value);
                    },
                },
            });

            skipSlider.noUiSlider.on("update", function (val, e) {
                skipValues[e].innerText = val[e];
            });
        }
    };

    /* Filter Product
    -------------------------------------------------------------------------*/
    var filterProducts = function () {
        const filters = {
            condition: null,
            brands: [],
            deal: false,
            starRate: null,
            priceRange: null,
            minPrice: null,
            maxPrice: null,
        };

        $('input[name="condition"]').change(function () {
            filters.condition = $(this).attr("id") === "inNew" ? "New" : "Old";
            applyFilters();
            updateMetaFilter();
        });
        $('input[name="deal"]').change(function () {
            filters.deal = $(this).attr("id") === "dealAll" ? "Deal All" : "Deal Today";
            applyFilters();
            updateMetaFilter();
        });
        $('input[name="brand"]').change(function () {
            const brandId = $(this).attr("id");
            let brandLabel = $(this).next("label").text().trim();
            brandLabel = brandLabel.replace(/\s*\(\d+\)$/, "");

            if ($(this).is(":checked")) {
                filters.brands.push({ id: brandId, label: brandLabel });
            } else {
                filters.brands = filters.brands.filter((brand) => brand.id !== brandId);
            }
            applyFilters();
            updateMetaFilter();
        });
        $('input[name="starRate"]').change(function () {
            filters.starRate =
                $(this).attr("id") === "fiveStar"
                    ? "5 Star"
                    : $(this).attr("id") === "fourStar"
                    ? "4 Star"
                    : $(this).attr("id") === "threeStar"
                    ? "3 Star"
                    : $(this).attr("id") === "twoStar"
                    ? "2 Star"
                    : "1 Star";
            applyFilters();
            updateMetaFilter();
        });

        $('input[name="price"]').change(function () {
            const priceId = $(this).attr("id");
            filters.priceRange = priceId;
            applyFilters();
            updateMetaFilter();
        });
        $(".btn-filter-price").click(function () {
            let minPrice = parseFloat($(".min-price").val());
            let maxPrice = parseFloat($(".max-price").val());

            if (isNaN(minPrice)) {
                minPrice = null;
            }

            if (isNaN(maxPrice)) {
                maxPrice = null;
            }

            if (minPrice !== null && minPrice < 0) {
                $(".min-price").val(0);
                minPrice = 0;
            }

            if (maxPrice !== null && maxPrice < 0) {
                $(".max-price").val(0);
                maxPrice = 0;
            }

            if (minPrice !== null && maxPrice !== null && minPrice > maxPrice) {
                maxPrice = minPrice + 1;
                $(".max-price").val(maxPrice);
            }

            filters.minPrice = minPrice;
            filters.maxPrice = maxPrice;
            applyFilters();
            updateMetaFilter();
        });
        function updateMetaFilter() {
            const appliedFilters = $("#applied-filters");
            const metaFilterShop = $(".meta-filter-shop");
            appliedFilters.empty();
            if (filters.condition) {
                appliedFilters.append(
                    `<span class="filter-tag">${filters.condition} <span class="remove-tag icon-close" data-filter="condition"></span></span>`
                );
            }
            if (filters.brands.length > 0) {
                filters.brands.forEach((brand) => {
                    appliedFilters.append(
                        `<span class="filter-tag">${brand.label} <span class="remove-tag icon-close" data-filter="brand" data-value="${brand.id}"></span></span>`
                    );
                });
            }
            if (filters.deal) {
                appliedFilters.append(
                    `<span class="filter-tag">${filters.deal} <span class="remove-tag icon-close" data-filter="deal"></span></span>`
                );
            }
            if (filters.starRate) {
                appliedFilters.append(
                    `<span class="filter-tag">${filters.starRate} <span class="remove-tag icon-close" data-filter="starRate"></span></span>`
                );
            }
            if (filters.priceRange) {
                const label = $("#" + filters.priceRange)
                    .next("label")
                    .text();
                appliedFilters.append(
                    `<span class="filter-tag">${label} <span class="remove-tag icon-close" data-filter="priceRadio"></span></span>`
                );
            }
            if (filters.minPrice !== null || filters.maxPrice !== null) {
                let priceFilterLabel = "";
                if (filters.minPrice !== null && filters.maxPrice !== null) {
                    priceFilterLabel = `$${filters.minPrice} - $${filters.maxPrice}`;
                } else if (filters.minPrice !== null) {
                    priceFilterLabel = `$${filters.minPrice} +`;
                } else {
                    priceFilterLabel = `$${filters.maxPrice} -`;
                }
                appliedFilters.append(
                    `<span class="filter-tag">${priceFilterLabel} <span class="remove-tag icon-close" data-filter="priceRangeInput"></span></span>`
                );
            }
            const hasFiltersApplied = appliedFilters.children().length > 0;
            metaFilterShop.toggle(hasFiltersApplied);

            $("#remove-all").toggle(hasFiltersApplied);
        }
        $("#applied-filters").on("click", ".remove-tag", function () {
            const filterType = $(this).data("filter");
            const filterValue = $(this).data("value");
            if (filterType === "condition") {
                filters.condition = null;
                $('input[name="condition"]').prop("checked", false);
            }
            if (filterType === "brand") {
                filters.brands = filters.brands.filter((brand) => brand.id !== filterValue);
                $(`input[name="brand"][id="${filterValue}"]`).prop("checked", false);
            }
            if (filterType === "deal") {
                filters.deal = null;
                $('input[name="deal"]').prop("checked", false);
            }
            if (filterType === "starRate") {
                filters.starRate = null;
                $('input[name="starRate"]').prop("checked", false);
            }
            if (filterType === "priceRadio") {
                filters.priceRange = null;
                $('input[name="price"]').prop("checked", false);
            }
            if (filterType === "priceRangeInput") {
                filters.minPrice = null;
                filters.maxPrice = null;
            }
            applyFilters();
            updateMetaFilter();
        });
        $("#remove-all,#reset-filter").click(function () {
            filters.condition = null;
            filters.brands = [];
            filters.deal = null;
            filters.starRate = null;
            filters.priceRange = null;
            filters.minPrice = null;
            filters.maxPrice = null;
            $('input[name="brand"]').prop("checked", false);
            $('input[name="condition"]').prop("checked", false);
            $('input[name="deal"]').prop("checked", false);
            $('input[name="starRate"]').prop("checked", false);
            $('input[name="price"]').prop("checked", false);
            $(".min-price").val("");
            $(".max-price").val("");
            applyFilters();
            updateMetaFilter();
        });
        function applyFilters() {
            let visibleProductCount = 0;
            let priceNew;
            $(".wrapper-shop .card-product").each(function () {
                const product = $(this);
                let showProduct = true;
                const priceNew = parseFloat(product.find(".new-price").text().replace("$", ""));

                if (filters.condition) {
                    const conditionStatus = product.data("condition");
                    if (filters.condition !== conditionStatus) {
                        showProduct = false;
                    }
                }
                if (filters.brands.length > 0) {
                    const brandId = product.attr("data-brand");
                    if (!filters.brands.some((brand) => brand.id === brandId)) {
                        showProduct = false;
                    }
                }
                let dealStatus = product.data("deal") || "Deal All";
                if (filters.deal && filters.deal !== dealStatus) {
                    showProduct = false;
                }

                if (filters.starRate) {
                    const starRateStatus = product.data("rate");
                    if (filters.starRate !== starRateStatus) {
                        showProduct = false;
                    }
                }
                if (filters.priceRange) {
                    switch (filters.priceRange) {
                        case "u10":
                            if (priceNew > 10) showProduct = false;
                            break;
                        case "u15":
                            if (priceNew < 10 || priceNew > 15) showProduct = false;
                            break;
                        case "u25":
                            if (priceNew < 15 || priceNew > 25) showProduct = false;
                            break;
                        case "up35":
                            if (priceNew < 35) showProduct = false;
                            break;
                    }
                }
                if (filters.minPrice !== null && priceNew < filters.minPrice) {
                    showProduct = false;
                }

                if (filters.maxPrice !== null && priceNew > filters.maxPrice) {
                    showProduct = false;
                }
                product.toggle(showProduct);
                if (showProduct) {
                    visibleProductCount++;
                }
            });
            $("#product-count-grid").html(`<span class="count">${visibleProductCount}</span> Products Found`);
            updateLastVisibleItem();

            if (visibleProductCount < 8) {
                $(".wd-load").addClass("d-none");
            } else {
                $(".wd-load").removeClass("d-none");
            }
        }
        function updateLastVisibleItem() {
            setTimeout(() => {
                $(".card-product.style-list").removeClass("last");
                const lastVisible = $(".card-product.style-list:visible").last();
                if (lastVisible.length > 0) {
                    lastVisible.addClass("last");
                }
            }, 50);
        }
    };

    /* Filter Sort
    -------------------------------------------------------------------------*/
    var filterSort = function () {
        let originalProductsGrid = $("#gridLayout .card-product").clone();
        $(".select-item").on("click", function () {
            const sortValue = $(this).data("sort-value");
            $(".select-item").removeClass("active");
            $(this).addClass("active");
            // $(".text-sort-value").text($(this).find(".text-value-item").text());

            applyFilter(sortValue);
        });

        function applyFilter(sortValue) {
            let products;
            let tabClass = $(".tf-view-layout-switch.active").data("tab");
            products = $("#gridLayout .card-product");
            function applyLayoutClasses(cards) {
                cards.each(function () {
                    if (tabClass === "tablist-1") {
                        $(this).addClass("style-row");
                    } else if (tabClass === "tablist-2") {
                        $(this).addClass("style-row type-row-2 row-small flex-sm-row");
                    }
                });
            }
            let sliceCount = 0;
            if (sortValue === "0-5") sliceCount = 5;
            else if (sortValue === "0-10") sliceCount = 10;
            else if (sortValue === "0-15") sliceCount = 15;
            else if (sortValue === "0-20") sliceCount = 20;
            else if (sortValue === "0-50") sliceCount = 50;

            if (sliceCount > 0) {
                $("#gridLayout").empty().append(originalProductsGrid.slice(0, sliceCount).clone());
                $(".meta-filter-shop").hide();
                applyLayoutClasses($("#gridLayout .card-product"));
                return;
            }
            if (sortValue === "best-selling") {
                $("#gridLayout .card-product").each(function (index) {
                    $(originalProductsGrid[index]).attr("class", $(this).attr("class"));
                });

                $("#gridLayout").empty().append(originalProductsGrid.clone());
                $(".meta-filter-shop").hide();
                return;
            }

            if (sortValue === "price-low-high") {
                products.sort(
                    (a, b) =>
                        parseFloat($(a).find(".new-price").text().replace("$", "")) -
                        parseFloat($(b).find(".new-price").text().replace("$", ""))
                );
            } else if (sortValue === "price-high-low") {
                products.sort(
                    (a, b) =>
                        parseFloat($(b).find(".new-price").text().replace("$", "")) -
                        parseFloat($(a).find(".new-price").text().replace("$", ""))
                );
            } else if (sortValue === "a-z") {
                products.sort((a, b) =>
                    $(a).find(".name-product").text().localeCompare($(b).find(".name-product").text())
                );
            } else if (sortValue === "z-a") {
                products.sort((a, b) =>
                    $(b).find(".name-product").text().localeCompare($(a).find(".name-product").text())
                );
            }

            $("#gridLayout").empty().append(products);
        }
    };

    /* Filer Loadmore
    -------------------------------------------------------------------------*/
    var loadmoreFilter = function () {
        var items = $(".facet-fieldset.has-loadmore .fieldset-item");
        var maxVisible = 7;

        items.slice(maxVisible).hide();

        $(".facet-fieldset.has-loadmore .btn-loadmore").on("click", function () {
            var hiddenItems = items.slice(maxVisible);
            hiddenItems.stop(true, true).slideDown(300, function () {
                $(".facet-fieldset.has-loadmore .btn-loadmore").remove();
            });
        });
    };

    /* Filter Price
    -------------------------------------------------------------------------*/
    var filterPrice = function () {
        $(".min-price, .max-price").on("focus", function () {
            $('input[name="price"]').prop("checked", false);
        });

        $(".btn-filter-price").on("click", function () {
            let minPrice = parseFloat($(".min-price").eq(0).val()) || 0;
            let maxPrice = parseFloat($(".min-price").eq(1).val()) || 0;

            if (maxPrice > 0 && minPrice > 0 && maxPrice <= minPrice) {
                alert("Max price must be greater than Min price!");
            }
        });
    };

    $(function () {
        rangeTwoPrice();
        filterProducts();
        filterSort();
        filterPrice();
        loadmoreFilter();
    });
})(jQuery);
