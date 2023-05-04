"""contains all Mailing feature functions"""
import subprocess

from flask import Blueprint, jsonify, request
from mailmerge import MailMerge
from docx2pdf import convert
from helpers import MailType

THUNDERBIRD_PATH = "C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe"

mailing_routes = Blueprint('simple_page', __name__, )


def send_mail(arg_mails, arg_mail_mode, arg_subject, arg_content, arg_attachments):
    """send mail"""

    execute_thunderbird = THUNDERBIRD_PATH + " -compose " + arg_mail_mode + "='" + \
        ",".join(arg_mails) + "'," + "subject='" + arg_subject + \
        "'," + "body='" + arg_content + "',"
    if len(arg_attachments) > 0:
        execute_thunderbird += "attachment='" + \
            arg_attachments[0] + "'"  # todo

    with subprocess.Popen(execute_thunderbird):
        pass


def send_massmail(arg_mails, arg_mail_mode, arg_subject, arg_content, arg_attachments):
    """send massmail"""
    send_mail(arg_mails, arg_mail_mode, arg_subject,
              arg_content, arg_attachments)


def send_personalized_mail(arg_csv_file, arg_mails,  arg_subject, arg_content, arg_attachments):
    """send personalized mail"""
    csv_cols = arg_csv_file[0].split(";")
    for mail_index, mail in enumerate(arg_mails):
        tmp_content = arg_content
        for col_index, col in enumerate(csv_cols):

            tmp_content = tmp_content.replace(
                "[$$$"+col+"$$$]", arg_csv_file[mail_index+1].split(";")[col_index])

        send_mail([mail], "to", arg_subject, tmp_content, arg_attachments)


def send_template_mail(arg_csv_file, arg_mails,  arg_subject, arg_content, arg_attachments):
    """send mail based on a word template"""
    csv_cols = arg_csv_file[0].split(";")
    for mail_index, _ in enumerate(arg_mails):
        template_file = r"..\template.docx"

        output_dir = "..\\"
        output_name = str(mail_index)+"test"
        output_docx = output_name + ".docx"
        # todo output_pdf = output_name + ".pdf"

        document = MailMerge(template_file)

        for col_index, col in enumerate(csv_cols):
            splitted_row = arg_csv_file[mail_index+1].split(";")
            document.merge_templates(
                [{col: splitted_row[col_index]}], separator='page_break')

        document.write(output_dir + output_docx)
        convert(output_dir + output_docx)
        # todo anhang = os.getcwd() + "\\..\\" + output_pdf
        send_personalized_mail(arg_csv_file, arg_mails,
                               arg_subject, arg_content, arg_attachments)


@mailing_routes.route("/api/test", methods=["POST"])
def merge_docx():
    """returns all participants as json"""

    mail_type = MailType(int(request.form.get("mailType")))
    subject = request.form.get("subject")
    content = request.form.get("content")
    mail = request.form.get("mail")

    mails = [mail]
    # csv_filehandle = request.files["csvFile"]

    # csv_file = csv_filehandle.read().decode("utf8").split("\r\n")
    # mail_index = csv_file[0].split(";").index("mail")
    # mails = []
    # for i, row in enumerate(csv_file):
    #    if i > 0 and row is not None and row != "":
    #        mail = row.split(";")[mail_index]
    #        mails.append(mail)

    if mail_type == MailType.MASS_MAIL:
        mail_mode = "bcc"
        if request.form.get("isBcc") is None:
            mail_mode = "to"
        send_massmail(mails, mail_mode, subject, content, [])
    elif mail_type == MailType.PERSONALIZED_MAIL:
        pass  # send_personalized_mail(csv_file, mails,  subject, content, [])
    elif mail_type == MailType.TEMPLATE_MAIL:
        pass  # send_template_mail(csv_file, mails,  subject, content, [])

    return jsonify("ok")
