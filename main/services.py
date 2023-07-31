from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from main.models import Mailing, LogiMail


def make_mailing(mailing, pk):
    mailing.status = Mailing.objects.filter('started')
    mailing.save()

    print(f'Рассылка {pk} запущена.')

    try:
        recipients = mailing.client.all()
        rec_list = [rec.email for rec in recipients]
        result = send_mail(
            subject=mailing.message.title,
            message=mailing.message.context,
            from_email=EMAIL_HOST_USER,
            recipient_list=rec_list,
            fail_silently=False
        )

        if result:
            mailing_log = LogiMail.objects.create(
                status=LogiMail.SUCCESS,
                answer=200,
                mailing_id=mailing.id
            )

            print(f'Сообщение отправлено. Отчет об успешной отправке {mailing_log.id} создан.')

        else:
            mailing_log = LogiMail.objects.create(
                status=LogiMail.FAIL,
                answer='Сообщение не отправлено (получателя нет либо указан неверный адрес почты)',
                mailing_id=mailing.id
            )

            print(f'Сообщение не отправлено. Отчет об неуспешной отправке {mailing_log.id} создан.')

    except Exception as error:
        mailing_log = LogiMail.objects.create(
            status=LogiMail.FAIL,
            answer=error,
            mailing_id=mailing.id
        )

        print(f'Сообщение не отправлено. Отчет об неуспешной отправке {mailing_log.id} создан.')