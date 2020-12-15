import random
from pprint import pprint
import datetime
import os
from flask import Flask, request, render_template_string, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():
    with open("templates/test.html") as inf:
        template = inf.read()
    # template = template.replace("{{body}}", str(os.listdir(".")))
    # template = template.replace("{{head}}", "<script src='static/test.js'></script>")
    # template = template.replace("{{head}}", "<script src='http://192.168.1.130:8081/test.js'></script>")
    template = template.replace("|||SAMPLE|||", "".join(random.choices("0123456789", k=10)))

    return render_template_string(template)


@app.route('/clear')
def cleanLog():
    with open("log", "w") as of:
        of.write("")
    pprint(request.__dict__)
    # return redirect(request.environ["HTTP_REFERER"])
    return redirect("/")


@app.route('/subpage')
def subpage():
    headparam = request.args.get("headparam")
    bodyparam = request.args.get("bodyparam")
    print(headparam)
    print(bodyparam)
    with open("templates/test.html") as inf:
        template = inf.read()

    with open("log", "r") as inf:
        log = inf.read()

    hp2 = headparam.replace("'", "\\'")
    bp2 = bodyparam.replace("'", "\\'")
    logString = f"""
    <code>
    __________________________________________
    {datetime.datetime.now().isoformat()}
    <b>Head</b>
    {headparam.replace("<", "&lt;")}
    <button type="button" onclick="reloadAttackTextHead('{hp2}')">Reuse This</button>

    <b>Body</b>
    {bodyparam.replace("<", "&lt;")}
    <button type="button" onclick="reloadAttackTextBody('{bp2}')">Reuse This</button>
    __________________________________________

    </code>
    """

    logString += log
    with open("log", "w") as of:
        log = of.write(logString)
    template = template.replace("{{head}}", headparam)
    template = template.replace("{{body}}", bodyparam)
    template = template.replace("{{log}}", logString.replace("\n", "\n<br>\n"))
    template = template.replace("|||SAMPLE|||", "".join(random.choices("0123456789", k=10)))
    return render_template_string(template)


app.run("0.0.0.0", 8888, debug=True)