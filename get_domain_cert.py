import dns.resolver
import argparse
import socket
import ssl
import OpenSSL
from datetime import datetime, timedelta, timezone

# 証明書から有効期限とシリアルナンバーを取得する。
def get_certificate_info(hostname):
    date_format, encoding = "%Y%m%d%H%M%S%z", "ascii"
    cert = get_server_certificate(hostname)
    if cert is None:
        return (hostname, None, None)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    serial_number = x509.get_serial_number()
    not_after_datetime = datetime.strptime(x509.get_notAfter().decode(encoding), date_format)
    jst = timezone(timedelta(hours=+9), 'JST')
    not_after_datetime = not_after_datetime.astimezone(jst)
    not_after = not_after_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    return {"hostname": hostname, "not_after":not_after, "serial_number":serial_number}

# 証明書の取得
def get_server_certificate(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                der_cert = sslsock.getpeercert(True)
                return ssl.DER_cert_to_PEM_cert(der_cert)
    except:
        return None
# Aレコードの存在チェック
def exist_a_record(hostname):
    try:
        answers = dns.resolver.resolve(hostname, "A")
        if answers is not None:
            return True
        else:
            return False
    except:
        return False

# ドメイン名と証明書情報を取得する。
def get_domain_name_cert(domai_names):
    # 処理対象のドメイン名を作成する。
    proc_domain_names = []
    for domain_name in domai_names:
        if exist_a_record(domain_name):
            proc_domain_names.append(domain_name)
    # 証明書情報を作成する。
    cert_info_names = []
    for proc_domain_name in proc_domain_names:
        cert_info_name = get_certificate_info(proc_domain_name)
        cert_info_names.append(cert_info_name)
    return cert_info_names

def main():
    # ホスト名のリストを取得する。
    host_names = []
    with open("list.txt") as f:
        for line in f:
            host_names.append(line.strip())
    domain_name_certs = get_domain_name_cert(host_names)
    for domain_name_cert in domain_name_certs:
        print(domain_name_cert)

if __name__=='__main__':
    main()