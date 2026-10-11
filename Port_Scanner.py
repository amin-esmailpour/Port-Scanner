import pyfiglet
import termcolor
import IPy

import os
import sys
import socket
import time
import threading

os.system("cls" if os.name=="nt" else "clear")

class PortScanner:
    print(termcolor.colored(text=pyfiglet.figlet_format("Port Scanner", font="big"), color=(57, 87, 195)))
    print(termcolor.colored(text="In This Port Scanner Tool\n\
You Can Enter One Or Multiple Addresses Or Path \
To A TXT File Containing Addresses.!!!!!!",
                            color=(57, 87, 195)))
    print()

    def __init__(self):
        self.addresses = []  # addresses list
        self.port_range = []  # port(s) list
        self.scan_speed = "normal"  # port scanning speed
        self.open_ports = {}  # dictionary
        self.percent = 0  # Number of ports scanned in percentage
        self.count = 0  # Number of ports scan
        self.banners = {}

    class Exit(Exception):
        pass

    def getting_address(self):
        while True:
            print(f"{termcolor.colored(text="[+]",
                                       color=(57, 87, 195))} Enter The "
                  f"{termcolor.colored(text="Target Addresses",
                                       color=(57, 87, 195))} : ",
                  end='')
            entered_address = input().lower().strip().replace(" ", "")

            if entered_address not in ["cls", "clear", "exit"]:
                try:  # A case where only one address is entered
                    # Checking whether the input string is an address or not
                    IPy.IP(socket.gethostbyname(entered_address))
                    self.addresses.append(entered_address)
                    break
                except socket.gaierror:
                    if entered_address.find(',') != -1:  # A case where multiple addresses is entered
                        for address in entered_address.split(","):
                            address = address.strip()
                            try:  # Checking whether the input string is an address or not
                                IPy.IP(socket.gethostbyname(address))
                                self.addresses.append(address)
                            except socket.gaierror:
                                pass
                        break

                    elif entered_address.endswith(
                            ".txt"):  # A case where a txt file containing addresses is entered
                        try:
                            with open(entered_address, 'r') as file:
                                for line in file.readlines():
                                    address = line.strip().strip("\n").replace(" ", "")
                                    try:  # Checking whether the input string is an address or not
                                        IPy.IP(socket.gethostbyname(address))
                                        self.addresses.append(address)
                                    except socket.gaierror:
                                        pass
                                    except ValueError:
                                        pass
                                file.close()
                            break
                        except FileNotFoundError:
                            print(f"{termcolor.colored(text="[!!] File Not Found.!!!!!!",
                                                       color="red")}")
                            print()
                            continue
                    else:
                        self.report_error(entered_address)  # Static method
                        continue
                except UnicodeEncodeError:
                    self.report_error(entered_address)  # Static method
                    continue
            elif entered_address in ["cls", "clear"]:
                os.system("cls" if os.name == "nt" else "clear")  # For clear the terminal
            elif entered_address == "exit":
                raise PortScanner.Exit()  # To exit the program
            else:
                self.report_error(entered_address)  # Static method
                continue

    def getting_port(self):
        while True:
            print(f"{termcolor.colored(text="[+]",
                                       color=(57, 87, 195))} Enter The",
                  f"{termcolor.colored(text="Range Of Ports",
                                       color=(57, 87, 195))}",
                  f"To Scan(Ex: {termcolor.colored(text="1-500",
                                                           color=(57, 87, 195))} or",
                  f"{termcolor.colored(text="443",
                                       color=(57, 87, 195))}",
                  f"or {termcolor.colored(text="80,443,...",
                                          color=(57, 87, 195))}) : ",
                  end='')
            entered_port = input().lower().strip().replace(" ", "")

            if entered_port not in ["cls", "clear", "exit"]:
                try:  # A case where only one port is entered
                    entered_port = int(float(entered_port))  # Checking whether the input string is a port or not
                    if entered_port in range(1, 65536):
                        self.port_range.append(entered_port)
                        break
                    else:
                        self.report_error(entered_port)  # Static method
                        continue

                except ValueError:
                    try:
                        if entered_port.find('-') != -1 and entered_port.count(
                                '-') == 1:  # A case where a range of ports is entered.
                            entered_port = [int(float(port)) for port in entered_port.split('-')]
                            entered_port.sort()
                            self.port_range = range(entered_port[0], entered_port[1] + 1)

                        elif entered_port.find(',') != -1 and entered_port.count(
                                ",") == 1:  # A case where multiple port is entered
                            self.port_range = [int(float(port)) for port in entered_port.split(",")]
                        else:
                            self.report_error(entered_port)  # Static method
                            continue

                        flag = True
                        for port in self.port_range:  # Static method
                            if port in range(1, 65536):
                                pass
                            else:
                                flag = False
                                break
                        if flag:
                            pass
                        else:
                            self.report_error(entered_port)  # Static method
                            continue
                        break
                    except ValueError:
                        self.report_error(entered_port)  # Static method
                        continue
                except UnicodeEncodeError:
                    self.report_error(entered_port)  # Static method
                    continue
            elif entered_port in ["cls", "clear"]:
                os.system("cls" if os.name == "nt" else "clear")  # For clear the terminal
            elif entered_port == "exit":
                raise PortScanner.Exit()  # To exit the program
            else:
                self.report_error(entered_port)  # Static method
                continue

    def getting_scan_speed(self):
        while True:
            print(f"{termcolor.colored(text="[+]",
                                       color=(57, 87, 195))} Select The",
                  f"{termcolor.colored(text="Scan Speed",
                                       color=(57, 87, 195))}(Ex:",
                  f"{termcolor.colored(text="\"normal\"",
                                       color=(57, 87, 195))} or",
                  f"{termcolor.colored(text="\"fast\"",
                                       color=(57, 87, 195))} or",
                  f"{termcolor.colored(text="\"very fast\"",
                                       color=(57, 87, 195))}) : ", end='')
            entered_scan_speed = input().lower().strip().replace(" ", "")

            if entered_scan_speed not in ["cls", "clear", "exit"]:
                if entered_scan_speed in ["normal", "fast", "veryfast", ""]:
                    if entered_scan_speed == "":
                        pass
                    else:
                        self.scan_speed = entered_scan_speed
                    break
                else:
                    self.report_error(entered_scan_speed)  # Static method
                    continue
            elif entered_scan_speed in ["cls", "clear"]:
                os.system("cls" if os.name == "nt" else "clear")  # For clear the terminal
            elif entered_scan_speed == "exit":
                raise PortScanner.Exit()
            else:
                self.report_error(entered_scan_speed)  # Static method
                continue
        print('_' * 70)
        print()

    def start(self):  # Start the main program
        for address in self.addresses:
            print(termcolor.colored(text=f"(ಠ_ಠ) Scanning ({address}).!!!!!",
                                    color=(57, 87, 195)))
            try:
                IPy.IP(address)
                print()
            except ValueError:
                print(f"{termcolor.colored(text="IPv4 :",
                                           color=(57, 87, 195))} {str(socket.gethostbyname(address))}")
                print()
            except socket.gaierror:
                continue

            threads = []
            for port in self.port_range:
                self.progress_bar()
                thread = (threading.Thread(target=self.port_scan,
                                           args=(address, port,)))
                thread.start()
                threads.append(thread)
                if self.scan_speed == "normal":
                    time.sleep(1)
                elif self.scan_speed == "fast":
                    time.sleep(0.5)
                else:
                    if len(self.port_range) in range(1, 100 + 1):
                        time.sleep(0.1)  # from time library
                    elif len(self.port_range) in range(101, 1000 + 1):
                        time.sleep(0.01)  # from time library
                    elif len(self.port_range) in range(1001, 10000 + 1):
                        time.sleep(0.001)
                    else:
                        time.sleep(0.0005)

            for thread in threads:
                thread.join()
            threads.clear()

            print(f"\r{" " * 55}\r", end='')

            if len(self.open_ports) != 0:
                for port, banner in self.open_ports.items():
                    try:
                        print(f"{termcolor.colored(text="[+]",
                                                   color="green")} Port",
                              f"{termcolor.colored(text=f"{port}({socket.getservbyport(int(port))})",
                                                   color=(57, 87, 195))}",
                              f"Is {termcolor.colored(text="Open",
                                                      color=(57, 87, 195))}.",
                              end='')
                    except OSError:
                        print(f"{termcolor.colored(text="[+]",
                                                   color="green")} Port",
                              f"{termcolor.colored(text=f"{port}",
                                                   color=(57, 87, 195))} Is {termcolor.colored(text="Open",
                                                                                               color=(57, 87, 195))}.",
                              end='')
                    if banner:
                        print(f"\t\t{termcolor.colored(text="Banner",
                                                       color="green")}"
                              f"\t ---> \t{termcolor.colored(text=banner,
                                                             color="green")}",
                              end='')
                    else:
                        print()
                        pass
                print()
                print(termcolor.colored(text=f"{str(len(self.open_ports))} Ports Is Open.!!!!!",
                                        color="green"))
            else:
                print(f"No Ports Are Open.!!!!!!")
            print('_' * 70)
            print()
            self.open_ports.clear()  # Clear the list for scanning the next target.
            self.percent = 0  # Reset the percent for scanning the next target.
            self.count = 0  # Reset the progress bar for the next target.

    def progress_bar(self):
        number = len(self.port_range)
        temp = number / 20
        self.count += 1
        self.percent += (100 / number)
        print(
            f"\r{termcolor.colored(text=str(self.count),
                                   color=(57, 87, 195))} Ports Scanned",
            f"\t{termcolor.colored(text=f"{'█' * int(self.count / temp)}",
                                   color=(57, 87, 195))}{'█' * int((number - self.count) / temp)} {round(self.percent)}%    ",
            end='',
            flush=True)

    def port_scan(self, ip_address, port):  # Start scanning ports
        try:
            sock = socket.socket()  # Creat a socket
            sock.settimeout(5)
            sock.connect((self.check_ip(ip_address), port))
            try:
                data = str(sock.recv(1024).decode().strip("\\r\\n"))
                self.open_ports[port] = data
                self.banners[(ip_address, port)] = data
            except socket.error:
                self.open_ports[port] = ''
            except UnicodeDecodeError:
                pass
            sock.close()
        except TimeoutError:
            pass
        except OSError:  # If you were not connected to the Internet
            pass

    @staticmethod
    def check_ip(target):
        try:
            IPy.IP(target)
            return target
        except ValueError:
            return str(socket.gethostbyname(target))

    def save_banners(self):
        def confirmation():
            if self.banners:
                while True:
                    print(f"Do You Want To {termcolor.colored(text="Save The Banners",
                                                              color=(57, 87, 195))}?(y/n) : ",
                          end='')
                    self.confirm = input().strip().lower()
                    if self.confirm not in ["exit", "cls", "clear"]:
                        if self.confirm.find('y') != -1:
                            saving_process()
                            break
                        elif self.confirm.find('n') != -1:
                            print('_' * 70)
                            print()
                            break
                    elif self.confirm in ["cls", 'clear']:
                        os.system("cls" if os.name == "nt" else "clear")  # For clear the terminal
                    elif self.confirm == "exit":
                        raise PortScanner.Exit()  # To exit the program
                    else:
                        self.report_error(self.confirm)  # Static method
                        continue
            else:
                pass

        def saving_process():  # Start the saving process
            while True:
                print()
                print(f"Enter The {termcolor.colored(text="Path",
                                                     color=(57, 87, 195))} To The",
                      f"{termcolor.colored(text="TXT File",
                                           color=(57, 87, 195))} To",
                      f"{termcolor.colored(text="Save The Banners",
                                           color=(57, 87, 195))}.")
                print(f"(Ex: C:\\Users\\Shredder\\Desktop\\....",
                      f"Or {termcolor.colored(text="Enter Cancel",
                                              color=(57, 87, 195))} To",
                      f"{termcolor.colored(text="Cancel Saving",
                                           color=(57, 87, 195))}) : ",
                      end='')
                txt_file_path = input().strip().lower()

                if txt_file_path not in ["cls", "clear", "cancel", "exit"]:
                    if txt_file_path.endswith(".txt"):
                        try:
                            with open(txt_file_path, 'a') as file:
                                for address, banner in self.banners.items():
                                    file.write(
                                        f"IP Address : {address[0]}\tPort : {address[1]}({socket.getservbyport(address[1])})"
                                        f"\tBanner\t--->\t{banner}")  # Save banners
                                file.close()
                            print()
                            print(
                                termcolor.colored(
                                    text=f"{str(len(self.banners.values()))} Banners Saved Successfully.",
                                    color="green"))
                            print('_' * 70)
                            break
                        except FileNotFoundError:
                            print(f"{termcolor.colored(text="[!!] Cannot Open The File.!!!!!!",
                                                       color="red")}")
                            print()
                            continue  # Try again to Enter the new path
                    else:  # txt_file_path.endswith(".txt") == False
                        print(termcolor.colored(text="The File Format Is Invalid.!!!!!!",
                                                color="red"))
                        print()
                        continue  # Try again to Enter the new path
                elif txt_file_path in ["cls", "clear"]:
                    os.system("cls" if os.name == "nt" else "clear")
                elif txt_file_path == "cancel":  # if txt_file_path == "cancel"
                    cancel_save_process()
                    break
                elif txt_file_path == "exit":
                    raise PortScanner.Exit()

        def cancel_save_process():
            while True:
                self.confirm = ''
                print(f"Do You Really Want To ",
                      f"{termcolor.colored(text="Cancel The Data Saving Process",
                                           color=(57, 87, 195))}?(y/n) : ",
                      end='')
                self.confirm = input().strip().lower()

                if self.confirm not in ["cls", "clear", "exit", "cancel"]:
                    if self.confirm.find('y'):
                        print()
                        print(termcolor.colored(text="The Process Of Saving Data Was Canceled.!!!!!!",
                                                color="green"))
                        print('_' * 70)
                    elif self.confirm.find('n'):
                        saving_process()
                        break
                    else:
                        self.report_error(self.confirm)  # Static method
                        continue
                elif self.confirm in ["cls", "clear"]:
                    os.system("cls" if os.name == "nt" else "clear")
                elif self.confirm == "cancel":  # if txt_file_path == "cancel"
                    saving_process()
                    break
                elif self.confirm == "exit":
                    raise PortScanner.Exit()

        confirmation()

    @staticmethod
    def report_error(argument):
        print(f"{termcolor.colored(text="[!!]",
                                   color="red")} {argument}",
              f"{termcolor.colored(text="Is Invalid Input.!!!!!!",
                                   color="red")}")
        print()

    def main(self):
        self.getting_address()
        self.getting_port()
        self.getting_scan_speed()  # For select the scan speed
        self.start()  # Start scanning
        self.save_banners()  # For saving useful data.


if __name__ == "__main__":
    while True:
        try:
            PortScanner().main()
        except PortScanner.Exit:
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(1)
