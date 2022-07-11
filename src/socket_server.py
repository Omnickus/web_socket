import socket
import random
import re



http_code = '100|101|102|103    \
            |200|201|202|203|204|205|206|207|208|226    \
            |300|301|302|303|304|305|307|308    \
            |400|401|402|403|404|405|406|407|408|409|410|411|412|413|414|415|416|417|418|421|422|423|424|425|426|428|429|431|451    \
            |500|501|502|503|504|505|506|507|508|510|511|'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    address_and_port = ('127.0.0.1', random.randint(40000, 65535) )
    print('WEB Socket start on: ', address_and_port)
    s.bind(address_and_port)
    s.listen(10)

    header = {}
    accept_list = []
    answer = {
    'header' : '',
    'method' : '',
    'request' : '',
    'status' : '',
    }

    while True:

        conn, addr = s.accept()

        if conn and addr:

            user_addr = str(conn.getsockname()[0])
            if user_addr not in accept_list:
                accept_list.append(user_addr)

            data = conn.recv(1024).decode("utf-8")
            if data:
                data = data.split('\n')
                header[user_addr] = data
                for ip in header:
                    for head in header[ip]:
                        if re.search( r'^[A-Z-a-z]+:', head ):
                            answer['header'] = answer['header'] + head + '</br>'
                        if re.search( r'^(GET|POST)', head ):
                            s_ans = head.split(' ')
                            answer['method'] = s_ans[0]
                            answer['request'] = s_ans[1]
                            if re.search( fr'\?(status)=({http_code})', head):
                                code = re.search( fr'\?(status)=({http_code})', head)[0]
                                code = code.split('=')[1]
                                if code in http_code:
                                    answer['status'] = code
                                else:
                                    answer['status'] = '200'
                            else:
                                answer['status'] = '200'

                conn.send(  f"HTTP/1.1 {str(answer['status'])} OK\n     \
                            Content-Length: 100\n    \
                            Connection: close\n     \
                            Content-Type: text/html\n\n \
                                <h1>Hello from OTUS!</h1>   \
                                <h2>HEADERS in request:</h2>   \
                                <p>{str(answer['header'])}</p>    \
                            </br></br>    \
                                <h2>Request method:</h2>   \
                                <p>{str(answer['method'])}</p>    \
                            </br></br>    \
                                <h2>Params request:</h2>   \
                                <p>{str(answer['request'])}</p>    \
                            ".encode("utf-8"))
                answer['header'] = ''

            if user_addr in accept_list:
                pass
            else:
                conn.close()

