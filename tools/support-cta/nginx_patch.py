import sys
f=sys.argv[1]; s=open(f).read()
a="    location ~* \\.md$ {\n"
assert s.count(a)==1 and "/feed.xml" not in s
add='''    # Agent layer + feeds (2026-10-19)
    location = /feed.xml {
        types { }
        default_type "application/rss+xml; charset=utf-8";
        add_header Access-Control-Allow-Origin "*" always;
        try_files $uri =404;
    }
    location = /feed.json {
        types { }
        default_type "application/feed+json; charset=utf-8";
        add_header Access-Control-Allow-Origin "*" always;
        try_files $uri =404;
    }
    # .well-known must be reachable despite the dot-path deny below (^~ wins over regex locations)
    location ^~ /.well-known/ {
        types { application/json json; text/plain txt; }
        default_type "text/plain";
        charset utf-8;
        charset_types application/json text/plain;
        add_header Access-Control-Allow-Origin "*" always;
        try_files $uri =404;
    }

'''
s=s.replace(a, add+a); open(f,"w").write(s); print("patched")
