import threading
import mock_server
import mock_PDU
import mock_midspan
import mock_Pis

threads = [
    threading.Thread(target=mock_server.publish_server_data),
    threading.Thread(target=mock_PDU.run),
    threading.Thread(target=mock_midspan.run),
    threading.Thread(target=mock_Pis.publish_rpi_data),
]

def main():
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
