from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Product, ProductImage
from .utils import send_telegram_photo

@receiver(post_save, sender=ProductImage)
def send_post_to_telegram(sender, instance, created, **kwargs):

    if not created or not instance.is_main:
        return

    product = instance.product
    description = (product.description or "")[:200]

    message = (
        f"🆕 <b>Yangi mahsulot!</b>\n"
        f"👉 <b>{product.title}</b>\n"
        f"💰 {product.price} so'm\n"
        f"<b>Mahsulot haqida:</b> {description}...\n"
        f"<b>Yuklangan sana:</b> {product.created_at}"
    )

    send_telegram_photo(instance.image.path, message)



