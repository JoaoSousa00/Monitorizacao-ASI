import os
import re


def getLogsInfo(path: str):
    """
    Contagem apartir dos ficheiros dos logs.

    :param path: Caminho da pasta que contêm os logs
    :type path: str

    Returns: Retorna um array com 4 valores:
        *Nº de Logs com status 200;

        *Nº de Logs com status 4XX;

        *Nº de Logs com status 5XX;

        *Nº de Logs do tipo '/wp-admin' com status entre 400 a 599.
    """
    pattern1 = re.compile(r"\s200\s")
    count_success = 0
    pattern2 = re.compile(r"\s4\d{2}\s")
    count_request_error = 0
    pattern3 = re.compile(r"\s5\d{2}\s")
    count_server_error = 0
    pattern4 = re.compile(r"^.*/wp-admin\sHTTP/1.0\"\s[4-5]\d{2}.*$")
    count_wp_admin_error = 0

    for f in os.listdir(path):
        if f.endswith(".log"):
            with open(path + "/" + f) as fp:
                for linha in fp:
                    match_success = pattern1.findall(linha)
                    match_request_error = pattern2.findall(linha)
                    match_server_error = pattern3.findall(linha)
                    match_wp_admin_error = pattern4.findall(linha)

                    if match_success:
                        count_success += 1
                    elif match_request_error:
                        count_success += 1
                    elif match_server_error:
                        count_server_error += 1

                    if match_wp_admin_error:
                        count_wp_admin_error += 1

    return {"200": str(count_success), "4xx": str(count_request_error), "5xx": str(count_server_error),
            "AdminError": str(count_wp_admin_error)}
