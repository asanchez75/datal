import logging

from django.conf import settings

from post_office import mail


class DjangoMailService:

    def __init__(self):
        pass

    @staticmethod
    def send_password_recovered_mail(user, password):
        """
        Envio correo con nueva clave

        :param user: User object
        :param password: Password string
        """
        email_data = dict(nick=user.nick, password=password)
        to = [user.email]

        template_name = 'password_recovered_{}'.format(user.language)

        try:
            mail.send(to, settings.DEFAULT_FROM_EMAIL, template=template_name, context=email_data,
                      priority='now')
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Failed to send email to {}. Error: {}".format(user.email, e.message))
            return False

    @staticmethod
    def send_forgot_password_mail(user, link):
        """
        Envio correo de cambio de clave

        :param user: User object
        :param link: URL String
        """
        email_data = dict(url=link)
        to = [user.email]

        template_name = 'reset_password_{}'.format(user.language)

        try:
            mail.send(to, settings.DEFAULT_FROM_EMAIL, template=template_name, context=email_data,
                      priority='now')
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Failed to send email to {}. Error: {}".format(user.email, e.message))
            return False

    @staticmethod
    def send_welcome_mail(user, link, company):
        """ Notify new admin """

        email_data = dict(
            name=user.name,
            admin_name=user.nick,
            company=company,
            link=link,
        )
        to = [user.email]

        template_name = 'activate_account_{}'.format(user.language)

        try:
            mail.send(to, settings.DEFAULT_FROM_EMAIL, template=template_name, context=email_data,
                      priority='now')
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Failed to send email to {}. Error: {}".format(user.email, e.message))
            return False

    def list_subscribe(self, user, language='es', extradata={}):
        return True
