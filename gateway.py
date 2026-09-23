from flask import Flask, request, Response
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from html import escape
import re

app = Flask(__name__)
 
@app.route('/')
def home():
    return '''
    <script>
setInterval(showTime, 1000);
const prog= document.getElementById("m")
function showTime() {
  const date = new Date();
  myDisplayer(date.toLocaleTimeString());
}

// Function to display any text
function myDisplayer(text) {
  demo.innerHTML = text;
}
function access(){
    const pwd = document.getElementById("pwd");
    const hidden = document.getElementById("hide");

    if(pwd.value === "123"){
   
        document.getElementById("hide").style.visibility = "visible";
    }else{
        alert("What's up bro?");
        alert("WRONG PASSWORD");
         alert("-- GAME OVER --");
    }
}
</script>
        <input type="password" id= "pwd" style="width:400px; padding:10px;" required><button id="sub" onclick="access()" style="padding:10px 20px; cursor:pointer;">submit</button>
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 100px; visibility:hidden;" id="hide">
        <h1 id= "demo"></h1><br><hr>
            <h2>Inter Portal Indirect Web Gateway</h2>
            <details>
                <summary>Credits About this Web Gateway</summary>
                <p>This web gateway/network was made to access all sites. First I was triying to use<br>
                an iframe to do it, but it did not work, so I desided to make a server. AI made the code<br>
                 while the idea was mine and, I chaneged some parts of the code.</p>
                 <img src="https://avatars.mds.yandex.net/i?id=750a893cc61b064e7162cbd4a80bf199da9d309f-4968350-images-thumbs&n=13">
                
            </details><br>
            <details>
                <summary>How to use</summary>
                <p>This aplication is quite easy to use. There are several ways and rules.<br> First, you have to put the <strong>complete</strong> url</p>
                
            </details>
            <details>
                <summary>Recomended Web Sites to load</summary>
                <form action="/view" method="get">
                    <input list= "sites" name= "url" style="width:400px; padding:10px;">
                        <datalist id="sites">
                        <option value ="https://yandex.ru/games/" >
                        <option value ="https://algebra.learnnexus.one/" >
                        <option value ="https://soupcan.pages.dev/iframe/" >
                        <option value ="https://blooket1.com" >
                        </datalist>
                    <button type="submit" style="padding:10px 20px; cursor:pointer;">Launch Page</button>
                </form>
            </details>
            <details>
                <summary>Load <strong>any</strong> Web Site </summary>
                    <p>You can load <b>any</b> web site in this gateway:</p>
                    <form action="/view" method="get">
                        <input type="url" name="url" placeholder="https://example.com" style="width:400px; padding:10px;" required>
                        <button type="submit" style="padding:10px 20px; cursor:pointer;">Launch Page</button>
                    </form>
                    <img src="https://avatars.mds.yandex.net/i?id=750a893cc61b064e7162cbd4a80bf199da9d309f-4968350-images-thumbs&n=13">
            </details>
            
            <a href="mailto:s34lev@students.bscr.ed.cr">Questions or Feedback<a>
        </div>
    '''

@app.route('/view')
def view():
    target_url = request.args.get('url')

    if not target_url:
        return """Missing URL | <a href="/">BACK</a>""", 400

    parsed_url = urlparse(target_url)

    if parsed_url.scheme not in ('http', 'https'):
        return "Only HTTP and HTTPS URLs are allowed", 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        req = Request(target_url, headers=headers)

        with urlopen(req, timeout=10) as res:
            content = res.read()
            status_code = res.status
            content_type = res.headers.get(
                "Content-Type",
                "application/octet-stream"
            )
            final_url = res.geturl()

        if 'text/html' in content_type.lower():
            base_tag = (
                f'<base href="{escape(final_url, quote=True)}">'
            ).encode('utf-8')

            head_pattern = rb'(<head\b[^>]*>)'

            if re.search(head_pattern, content, flags=re.IGNORECASE):
                content = re.sub(
                    head_pattern,
                    lambda match: match.group(1) + base_tag,
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
            else:
                content = base_tag + content

        return Response(
            content,
            status=status_code,
            content_type=content_type
        )

    except HTTPError as error:
        return f"HTTP error: {error.code}", error.code

    except URLError as error:
        return f"URL error: {error.reason}", 502

    except Exception as error:
        return f"Error proxying website: {error}", 500

if __name__ == '__main__':
    app.run(debug=True)
