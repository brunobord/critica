import smtplib
import MimeWriter
import mimetools
import StringIO
from datetime import datetime
from django.template import Context, loader
from django.conf import settings
from critica.apps.newsletter.models import Newsletter, NewsletterContent, Subscriber


def sendHtmlMail(email_from, email_to, subject, text, html):
    """
    Sends emails.
    
    """
    encoding = "quoted-printable"
    charset = "utf-8"

    out = StringIO.StringIO() 
    htmlin = StringIO.StringIO(html.encode('utf-8'))
    txtin = StringIO.StringIO(text.encode('utf-8'))
                          
    writer = MimeWriter.MimeWriter(out)
    writer.addheader("Subject", subject)
    writer.addheader("To", email_to)

    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()
                
    textPart = writer.nextpart()
    textPart.addheader("Content-Transfer-Encoding", encoding)
    pout = textPart.startbody("text/plain", [("charset", charset)])
    mimetools.encode(txtin, pout, encoding)
    txtin.close()
                                                                        
    htmlPart = writer.nextpart()
    htmlPart.addheader("Content-Transfer-Encoding", encoding)
    pout = htmlPart.startbody("text/html", [("charset", charset)])
    mimetools.encode(htmlin, pout, encoding)
    htmlin.close()
                        
    writer.lastpart()
    mail = out.getvalue()
    out.close()
    smtp = smtplib.SMTP("localhost")
    smtp.sendmail(email_from, [email_to], mail.encode('utf-8'))
    smtp.close()



def generate_newsletter(email, newsletter, subscriber):
    """ 
    Builds the newsletter. 
    
    """
    articles = NewsletterContent.objects.filter(newsletter=newsletter).order_by('order')
    
    html_template = loader.get_template('newsletter/email.html')
    html_context = Context({
        'articles': articles,
        'newsletter': newsletter,
        'subcriber': subscriber,
    })
    email_html = html_template.render(html_context)

    plain_template = loader.get_template('newsletter/email.txt')
    plain_context = Context({
        'articles': articles,
        'newsletter': newsletter,
        'subscriber': subscriber,
    })
    email_plain = plain_template.render(plain_context)
    
    sender.send_mail("news@critica.fr", email, "!TEST! (New)Critica newsletter !TEST!", email_plain, email_html)
    
    subscriber.last_newsletter = newsletter
    subscriber.save()
    
    newsletter.recipient_count = newsletter.recipient_count + 1
    newsletter.save()



def subscribers_loop():
    """
    Sends newsletter to subscribers.
    
    """
    newsletters = Newsletter.objects.filter(is_published=True, sending_start_date__isnull=True).order_by('sending_date')
    for newsletter in newsletters:
        if newsletter.sending_start_date == None:
            newsletter.sending_start_date = datetime.now()
            newsletter.save()

        newsletter_subscribers = Subscriber.objects.filter(is_active=True).exclude(last_newsletter=newsletter)
        for subscriber in newsletter_subscribers:
            generate_newsletter(subscriber.email, newsletter, subscriber)

        newsletter_subscribers = Subscriber.objects.filter(is_active=True, last_newsletter__isnull=True)
        for subscriber in newsletter_subscribers:
            generate_newsletter(subscriber.email, newsletter, subscriber)

        newsletter.sending_end_date = datetime.now()
        newsletter.save()


