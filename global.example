global
	log 		127.0.0.1 local0 info
	maxconn		4096
	#chroot		/usr/share/haproxy
	user		haproxy
	group		haproxy
	daemon
	stats		socket /etc/haproxy/socket level admin
	#debug
	#quiet

defaults
	log			global
	mode		http
	balance		roundrobin
	option		httplog
	option		dontlognull
	option		httpclose
	option 		forwardfor
	option		redispatch
	retries		3
	contimeout	5000
	clitimeout	50000
	srvtimeout	50000

listen app 0.0.0.0:80
	#cookie SERVERID rewrite
	stats enable
	stats scope .
	stats realm Haproxy\ Statistics
	stats refresh 10s
	stats hide-version
	stats uri /secret-haproxy-stats
	stats auth admin:webnotes
	option		httpchk GET /LatdA6 HTTP/1.1\r\nHost:\ www
	{{BACKEND}} check inter 20000

listen proxy 0.0.0.0:8080
