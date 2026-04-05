$(".tf-sw-categories").each(function (index, element) {
    var $this = $(element);
    var preview = $this.data("preview");
    var tablet = $this.data("tablet");
    var mobile = $this.data("mobile");
    var mobileSm = $this.data("mobile-sm") !== undefined ? $this.data("mobile-sm") : mobile;
    var spacingLg = $this.data("space-lg");
    var spacingMd = $this.data("space-md");
    var spacing = $this.data("space");
    var perGroup = $this.data("pagination") || 1;
    var perGroupMd = $this.data("pagination-md") || 1;
    var perGroupLg = $this.data("pagination-lg") || 1;
    var loop = $this.data("loop") !== undefined ? $this.data("loop") : false;
    var centered = $this.data("centered") !== undefined ? $this.data("centered") : false;

    new Swiper($this[0], {
        slidesPerView: mobile,
        spaceBetween: spacing,
        speed: 1000,
        pagination: {
            el: $this.find(".sw-pagination-categories")[0],
            clickable: true,
        },
        slidesPerGroup: perGroup,
        observer: true,
        centeredSlides: centered,
        observeParents: true,
        navigation: {
            nextEl: $this.find(".nav-next-categories")[0],
            prevEl: $this.find(".nav-prev-categories")[0],
            clickable: true,
        },
        loop: loop,
        breakpoints: {
            575: {
                slidesPerView: mobileSm,
                spaceBetween: spacing,
                slidesPerGroup: perGroup,
            },
            768: {
                slidesPerView: tablet,
                spaceBetween: spacingMd,
                slidesPerGroup: perGroupMd,
            },
            1200: {
                slidesPerView: preview,
                spaceBetween: spacingLg,
                slidesPerGroup: perGroupLg,
            },
        },
    });
});
if ($(".tf-sw-products").length > 0) {
    $(".tf-sw-products").each(function (index, element) {
        var $this = $(element);
        var preview = $this.data("preview") || 1;
        var tablet = $this.data("tablet") || 1;
        var mobile = $this.data("mobile") || 1;
        var mobileSm = $this.data("mobile-sm") !== undefined ? $this.data("mobile-sm") : mobile;
        var spacingLg = $this.data("space-lg") || 0;
        var spacingMd = $this.data("space-md") || 0;
        var spacing = $this.data("space") || 0;
        var perGroup = $this.data("pagination") || 1;
        var perGroupSm = $this.data("pagination-sm") || 1;
        var perGroupMd = $this.data("pagination-md") || 1;
        var perGroupLg = $this.data("pagination-lg") || 1;
        var gridRows = $this.data("grid") || 1; //

        var swiper = new Swiper($this[0], {
            speed: 800,
            slidesPerView: mobile,
            spaceBetween: spacing,
            slidesPerGroup: perGroup,
            grid: {
                rows: gridRows,
                fill: "row",
            },
            pagination: {
                el: $this.find(".sw-pagination-products")[0],
                clickable: true,
            },
            observer: true,
            observeParents: true,
            navigation: {
                nextEl: [
                    $this.closest(".container, .box-btn-slide-item").find(".nav-next-products")[0],
                    $this.closest(".box-btn-slide-2").find(".nav-next-products-2")[0],
                ],
                prevEl: [
                    $this.closest(".container, .box-btn-slide-item").find(".nav-prev-products")[0],
                    $this.closest(".box-btn-slide-2").find(".nav-prev-products-2")[0],
                ],
            },
            breakpoints: {
                575: {
                    slidesPerView: mobileSm,
                    spaceBetween: spacing,
                    slidesPerGroup: perGroupSm,
                    grid: {
                        rows: gridRows,
                        fill: "row",
                    },
                },
                768: {
                    slidesPerView: tablet,
                    spaceBetween: spacingMd,
                    slidesPerGroup: perGroupMd,
                    grid: {
                        rows: gridRows,
                        fill: "row",
                    },
                },
                1200: {
                    slidesPerView: preview,
                    spaceBetween: spacingLg,
                    slidesPerGroup: perGroupLg,
                    grid: {
                        rows: gridRows,
                        fill: "row",
                    },
                },
            },
        });
    });
}

if ($(".tf-sw-iconbox").length > 0) {
    $(".tf-sw-iconbox").each(function (index, element) {
        var $this = $(element);
        var preview = $this.data("preview") || 1;
        var previewXxl = $this.data("preview-xxl") || preview;
        var tablet = $this.data("tablet") || 1;
        var mobile = $this.data("mobile") || 1;
        var mobileSm = $this.data("mobile-sm") !== undefined ? $this.data("mobile-sm") : mobile;
        var spacingLg = $this.data("space-lg") || 0;
        var spacingMd = $this.data("space-md") || 0;
        var spacing = $this.data("space") || 0;
        var gridRows = $this.data("grid") || 1;
        var swiper = new Swiper($this[0], {
            slidesPerView: mobile,
            spaceBetween: spacing,
            speed: 1000,
            grid: {
                rows: 1,
                fill: "row",
            },
            pagination: {
                el: ".sw-pagination-iconbox",
                clickable: true,
            },
            observer: true,
            observeParents: true,
            navigation: {
                clickable: true,
                nextEl: ".nav-next-iconbox",
                prevEl: ".nav-prev-iconbox",
            },
            breakpoints: {
                575: {
                    slidesPerView: mobileSm,
                    spaceBetween: spacingMd,
                    grid: {
                        rows: 1,
                        fill: "row",
                    },
                },
                768: {
                    slidesPerView: tablet,
                    spaceBetween: spacingMd,
                    grid: {
                        rows: 1,
                        fill: "row",
                    },
                },
                1200: {
                    slidesPerView: previewXxl,
                    spaceBetween: spacingLg,
                    grid: {
                        rows: gridRows,
                        fill: "row",
                    },
                },
                1600: {
                    slidesPerView: preview,
                },
            },
        });
    });
}

if ($(".product-thumb-slider").length > 0) {
    $(".product-thumb-slider").each(function (index, element) {
        var $slider = $(element);
        var $thumbs = $slider.find(".tf-product-view-thumbs");
        var $main = $slider.find(".tf-product-view-main");
        var direction = $thumbs.data("direction") || "horizontal";
        var thumbs = new Swiper($thumbs[0], {
            direction: "horizontal",
            spaceBetween: 10,
            slidesPerView: "auto",
            freeMode: true,
            watchSlidesProgress: true,
            observer: true,
            observeParents: true,
            nested: true,
            breakpoints: {
                0: {
                    direction: "horizontal",
                },
                576: {
                    direction: direction,
                },
            },
        });

        var mainSwiper = new Swiper($main[0], {
            spaceBetween: 10,
            observer: true,
            observeParents: true,
            speed: 800,
            thumbs: {
                swiper: thumbs,
            },
            navigation: {
                nextEl: $slider.find(".single-slide-next")[0],
                prevEl: $slider.find(".single-slide-prev")[0],
            },
        });

        $thumbs.find(".swiper-slide").on("mouseenter", function () {
            let index = $(this).index();
            mainSwiper.slideTo(index);
        });
    });
}
if ($(".tf-single-slide").length > 0) {
    var main = new Swiper(".tf-single-slide", {
        slidesPerView: 1,
        spaceBetween: 0,
        observer: true,
        observeParents: true,
        speed: 800,
        navigation: {
            nextEl: ".single-slide-next",
            prevEl: ".single-slide-prev",
        },
    });
}
