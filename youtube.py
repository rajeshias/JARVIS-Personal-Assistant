import urllib.parse
import webbrowser
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
webbrowser.register(
    'chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def you(textToSearch):
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    webbrowser.get('chrome').open_new_tab(url)

if __name__ == '__main__':
    you('any text')
