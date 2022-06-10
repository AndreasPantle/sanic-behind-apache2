# sanic-behind-apache2

This projects demonstrates the use of Python Sanic behind an Apache2 with reverse proxy. Actually it is for testing purposes. The Sanic application itself makes not much sense. There are some API endpoints defined which can be called in a Browser or with curl.

## Testing

Of course you can test the Sanic application in a save environment. Please note you have to install Sanic first.

```bash
$ python3 -m pip install sanic --user
$ python3 usr/share/sanicbehindapache/main.py
```

## Server installation

Just prepare the server with an Apache 2 installation:

```bash
$ sudo apt install apache2 -y
$ sudo systemctl start apache2
$ sudo systemctl status apache2
$ sudo systemctl enable apache2
```

You should be able to see the default page: [http://ip-address:80](http://ip-address:80)

In addition to that you need the **rewrite** and the **proxy_http** module:

```bash
$ sudo a2enmod rewrite
$ sudo a2enmod proxy_http
```

## Put the Sanic application onto the server

Now the Sanic application should run as www-data user. You can of course put it at another user or create a new one. I would not recommend to use the root user in generally.

```bash
$ sudo -u www-data python3 -m pip install sanic
$ sudo -u www-data mkdir /usr/share/sanicbehindapache

# Copy or paste the main.py from the repository
$ sudo -u www-data nano /usr/share/sanicbehindapache/main.py

# Do a short test if it is running with the specified user
$ sudo -u www-data python3 /usr/share/sanicbehindapache/main.py
```

## Configuration of Apache2

After the application is running in his environment, we have to configure Apache2. I like the way with the configuration files. Each application is getting an own config file which could be enabled or disabled seperatly.

```bash
$ sudo nano /etc/apache2/conf-available/sanicbehindapache.conf
$ sudo a2enconf sanicbehindapache.conf
$ sudo systemctl reload apache2
```

This is basically the configuration for getting Apache2 to pass the traffic from [https://yourdomain.com/sanicbehindapache](https://yourdomain.com/sanicbehindapache) to [http://localhost:61210/](http://localhost:61210/) and back.

```conf
RewriteEngine on
RewriteCond %{HTTP_REFERER} ^https?://[^/]+/sanicbehindapache
RewriteCond %{REQUEST_URI} !^/sanicbehindapache
RewriteCond %{THE_REQUEST} ^GET
RewriteRule ^/(.*) /sanicbehindapache/$1 [QSA,R]
ProxyPass /sanicbehindapache/ http://localhost:61210/
ProxyPassReverse /sanicbehindapache/ http://localhost:61210/
Redirect permanent /sanicbehindapache https://yourdomainname.com/sanicbehindapache/
```

Of course you can check the documentation for further information about this conf file:

* [https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewriteengine](https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewriteengine)
* [https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewritecond](https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewritecond)
* [https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewriterule](https://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewriterule)
  * [https://httpd.apache.org/docs/current/rewrite/flags.html#flag_qsa](https://httpd.apache.org/docs/current/rewrite/flags.html#flag_qsa)
* [https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypass](https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypass)
  * [https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypassreverse](https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypassreverse)

## Enquiry the Sanic application

You can actually use this endpoints:

```bash
$ curl https://yourdomainname.com/sanicbehindapache/api/one/status
$ curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST https://yourdomainname.com/sanicbehindapache/api/one/echo
$ curl -X PUT https://yourdomainname.com/sanicbehindapache/api/one/change/55
$ curl -X DELETE https://yourdomainname.com/sanicbehindapache/api/one/remove/22
$ curl https://yourdomainname.com/sanicbehindapache/api/two/status
```
