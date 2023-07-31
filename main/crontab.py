from datetime import datetime, timedelta
from main.models import Mailing, LogiMail
from main.services import make_mailing


def daily_send():
    now = datetime.now()
    to_send = False

    for mail in Mailing.objects.filter(is_active=True, status='created' or 'started'):
        if mail.mailing_time.strftime('%H:%M') == now.strftime('%H:%M'):
            last_item = LogiMail.objects.filter(mailing=mail.id).last()
            if not last_item:
                to_send = True
            else:
                from_last = now.date() - last_item.date_last.date()
                if mail.periodicity == 'monthly' and from_last == timedelta(days=30) or mail.periodicity == 'weekly' and from_last == timedelta(days=7) or mail.periodicity == 'daily' and from_last == timedelta(days=1):
                    to_send = True
        if to_send:
            make_mailing(mail)


