import imapclient
import imaplib
import bs4
import pyzmail
import webbrowser


def unsubscribe(imap_address, email_address, password):
    """
    Checks unsubscribe links within emails and opens link to unsubscribe
    """
    imaplib._MAXLINE = 10000000
    imapObj = imapclient.IMAPClient(imap_address, ssl=True)
    imapObj.login(email_address, password)
    imapObj.select_folder('INBOX', readonly=True)
    UIDs = imapObj.search(['ALL'])

    for u in UIDs:
        rawMessages = imapObj.fetch([u], ['BODY[]', 'FLAGS'])
        message = pyzmail.PyzMessage.factory(rawMessages[u][b'BODY[]'])

        if message.html_part:
            html = message.html_part.get_payload().decode(message.html_part.charset)
            soup = bs4.BeautifulSoup(html, 'html.parser')
            linkElems = soup.select('a')

            for link in linkElems:
    
                if 'unsubscribe' in link.text.lower():
                    url = link.get('href')
                    print('opening {}: '.format(url))
                    webbrowser.open(url)

    imapObj.logout()


if __name__ == "__main__":

    email = input('Enter your email: ')
    password = input('Enter your email password: ')

    unsubscribe('imap.gmail.com', email, password)