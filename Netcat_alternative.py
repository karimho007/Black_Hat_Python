import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# main function responsible for handling command-line arguments and calling the rest of functions
def usage():
  print "BHP Net Tool"
  print
  print "Usage: bhpnet.py -t target_host -p port"
  print "-l --listen - listen on [host]:[port] for incoming connections"
  print "-e --execute=file_to_run - execute the given file upon receiving a connection"
  print "-c --command - initialize a command shell"
  print "-u --upload=destination - upon receiving connection upload a file and write to [destination]"
  print
  print
  print "Examples: "
  print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
  print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
  print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
  print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
  sys.exit(0)
  
  
  
def client_sender(buffer):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    # connect to our target host
    client.connect((target,port))
    
    # setting up our TCP socket object and then test to see if we have received any input from stdin
    if len(buffer):
      client.send(buffer)
    while True:
      # now wait for data back
      recv_len = 1
      response = ""
      
    # If all is well, we ship the data off to the remote target and receive back data until there is no more data to receive
      while recv_len:
        data = client.recv(4096)
        recv_len = len(data)
        if recv_len < 4096:
          break
      print response,
      
      # We then wait for further input from the user and continue sending and receiving data until the user kills the script
      buffer = raw_input("")
      buffer += "\n"
      
      # send it off
      client.send(buffer)
      
  except:
    print "[*] Exception! Exiting."
    # tear down the connection
    client.close()
      
  
  
  
def main():
  global listen
  global port
  global execute
  global command
  global upload_destination
  global target
  
  if not len(sys.argv[1:]):
    usage()
  # read the commandline options
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
  except getopt.GetoptError as err:
    print str(err)
    usage()
  for o,a in opts:
    if o in ("-h","--help"):
      usage()
    elif o in ("-l","--listen"):
      usage()
    elif o in ("-e", "--execute"):
      execute = a
    elif o in ("-c", "--commandshell"):
      command = True
    elif o in ("-u", "--upload"):
      upload_destination = a
    elif o in ("-t", "--target"):
      target = a
    elif o in ("-p", "--port"):
      port = int(a)
    else:
      assert False,"Unhandled Option"
      
  # are we going to listen or just send data from stdin?
  if not listen and len(target) and port > 0:
    
    # read in the buffer from the commandline
    # this will block, so send CTRL-D if not sending input
    # to stdin
    buffer = sys.stdin.read()
    
    # send data off
    client_sender(buffer)
    
  # we are going to listen and potentially
  # upload things, execute commands, and drop a shell back
  # depending on our command line options above
 
  if listen:
    ## detect that we are to set up a listening socket and process further commands (upload a file, execute a command, start a command shell).
    server_loop()
    
main()
