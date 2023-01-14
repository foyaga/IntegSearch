# -*- coding = utf-8 -*-
# @Time  : 2022/12/29 14:08
# @Author: Ifory
# @File  : query_syntax.py
from prettytable import PrettyTable


def query_syntax(qtype):
    fofa_query_syntax = [('title="beijing"', '从标题中搜索“北京”'), ('header="elastic"', '从http头中搜索“elastic”'),
                         ('body="网络空间测绘"', '从html正文中搜索“网络空间测绘”'), ('fid="sSXXGNUO2FefBTcCLIT/2Q=="', '查找相同的网站指纹'),
                         ('domain="qq.com"', '搜索根域名带有qq.com的网站'), ('icp="京ICP证030173号"', '查找备案号为“京ICP证030173号”的网站'),
                         ('js_name="js/jquery.js"', '查找网站正文中包含js/jquery.js的资产'),
                         ('js_md5="82ac3f14327a8b7ba49baa208d4eaa15"', '查找js源码与之匹配的资产'),
                         ('cname="ap21.inst.siteforce.com"', '查找cname为"ap21.inst.siteforce.com"的网站'),
                         ('cname_domain="siteforce.com"', '查找cname包含“siteforce.com”的网站'),
                         ('cloud_name="Aliyundun"', '通过云服务名称搜索资产'),
                         ('icon_hash="-247388890"', '搜索使用此 icon 的资产'), ('host=".gov.cn"', '从url中搜索”.gov.cn”'),
                         ('port="6379"', '查找对应“6379”端口的资产'), ('ip="1.1.1.1"', '从ip中搜索包含“1.1.1.1”的网站'),
                         ('ip="220.181.111.1/24"', '查询IP为“220.181.111.1”的C网段资产'),
                         ('status_code="402"', '查询服务器状态为“402”的资产'),
                         ('protocol="quic"', '查询quic协议资产'),
                         ('country="CN"', '搜索指定国家(编码)的资产'),
                         ('region="Xinjiang Uyghur Autonomous Region"', '搜索指定行政区的资产。'),
                         ('city="Ürümqi"', '搜索指定城市的资产。'),
                         ('cert="baidu"', '搜索证书(https或者imaps等)中带有baidu的资产。'),
                         ('cert.subject="Oracle Corporation"', '搜索证书持有者是Oracle Corporation的资产'),
                         ('cert.issuer="DigiCert"', '搜索证书颁发者为DigiCert Inc的资产'),
                         ('cert.is_valid=true', '验证证书是否有效，true有效，false无效'), ('jarm="2ad...83e81"', '搜索JARM指纹'),
                         ('banner="users" && protocol="ftp"', '搜索FTP协议中带有users文本的资产。'),
                         ('type="service"', '搜索所有协议资产，支持subdomain和service两'),
                         ('os="centos"', '搜索CentOS资产。'), ('server=="Microsoft-IIS/10"', '搜索IIS 10服务器。'),
                         ('app="Microsoft-Exchange"', '搜索Microsoft-Exchange设备'),
                         ('after="2017" && before="2017-10-01"', '时间范围段搜索'),
                         ('asn="19551"', '搜索指定asn的资产'),
                         ('org="LLC Baxet"', '搜索指定org(组织)的资产。'), ('base_protocol="udp"', '搜索指定udp协议的资产。'),
                         ('is_fraud=false', '排除仿冒/欺诈数据'), ('is_honeypot=false', '排除蜜罐数据'),
                         ('is_ipv6=true', '搜索ipv6的资产'),
                         ('is_domain=true', '搜索域名的资产'), ('is_cloud=true', '筛选使用了云服务的资'),
                         ('port_size="6"', '查询开放端口数量等于"6"的资产'),
                         ('port_size_gt="6"', '查询开放端口数量大于"6"的资产'), ('port_size_lt="12"', '查询开放端口数量小于"12"的资产'),
                         ('ip_ports="80,161"', '搜索同时开放80和161端口的ip'), ('ip_country="CN"', '搜索中国的ip资产(以ip为单位的资产数据)。'),
                         ('ip_region="Zhejiang"', '搜索指定行政区的ip资产(以ip为单位的资产数据)。'),
                         ('ip_city="Hangzhou"', '搜索指定城市的ip资产(以ip为单位的资产数据)。'),
                         ('ip_after="2021-03-18"', '搜索2021-03-18以后的ip资产(以ip为单位的资产数据)。'),
                         ('ip_before="2019-09-09"', '搜索2019-09-09以前的ip资产(以ip为单位的资产数据)。'),
                         ('=', '匹配，=""时，可查询不存在字段或者值为空的情况'),
                         ('==', '完全匹配，==""时，可查询存在且值为空的情况'), ('&&', '与'),
                         ('||', '或者'), ('!=', '不匹配，!=""时，可查询值为空的情况'), ('～=', '正则语法匹配专用（高级会员独有，不支持body）'),
                         ('()', '认查询优先级，括号内容优先级最高'), ]

    hunter_query_syntax = [('icp.web_name=”奇安信”', '搜索ICP备案网站名中含有“奇安信”的资产'), ('icp.type=”企业”', '搜索ICP备案主体为“企业”的资产'),
                           ('icp.name=”奇安信”', '搜索ICP备案单位名中含有“奇安信”的资产'),
                           ('icp.number=”京ICP备16020626号-8″', '通过域名关联ICP备案号为”京ICP备16020626号-8”的网站资产'),
                           ('domain=”qq.com”', '搜索域名包含”qq.com”的网站'), ('domain.suffix=”qq.com”', '搜索主域为qq.com的网站'),
                           ('is_domain=true', '搜索域名标记不为空的资产'), ('app.type=”开发与运维”', '查询包含组件分类为”开发与运维”的资产'),
                           ('app.name=”小米 Router”', '搜索标记为”小米 Router“的资产'), ('app.vendor=”PHP”', '查询包含组件厂商为”PHP”的资产'),
                           ('app.version=”1.8.1″', '查询包含组件版本为”1.8.1″的资产'),
                           ('header=”elastic”', '搜索HTTP请求头中含有”elastic“的资产'),
                           ('header.status_code=”402″', '搜索HTTP请求返回状态码为”402”的资产'),
                           ('header.server==”Microsoft-IIS/10″', '搜索server全名为“Microsoft-IIS/10”的服务器'),
                           ('header.content_length=”691″', '搜索HTTP消息主体的大小为691的网站'),
                           ('web.body=”网络空间测绘”', '搜索网站正文包含”网络空间测绘“的资产'),
                           ('web.title=”北京”', '从网站标题中搜索“北京”'),
                           ('web.similar_icon==”17262739310191283300″', '查询网站icon与该icon相似的资产'),
                           ('web.icon=”22eeab765346f14faf564a4709f98548″', '查询网站icon与该icon相同的资产'),
                           ('web.similar_id=”3322dfb483ea6fd250b29de488969b35″', '查询与该网页相似的资产'),
                           ('web.similar=”baidu.com:443″', '查询与baidu.com:443网站的特征相似的资产'),
                           ('after=”2021-01-01″ && before=”2021-12-21″', '搜索2021年的资产'),
                           ('cert=”baidu”', '搜索证书中带有baidu的资产'),
                           ('protocol=”http”', '搜索协议为”http“的资产'), ('protocol.transport=”udp”', '搜索传输层协议为”udp“的资产'),
                           ('protocol.banner=”nginx”', '查询端口响应中包含”nginx”的资产'),
                           ('as.number=”136800″', '搜索asn为”136800″的资产'),
                           ('as.name=”CLOUDFLARENET”', '搜索asn名称为”CLOUDFLARENET”的资产'),
                           ('as.org=”PDR”', '搜索asn注册机构为”PDR”的资产'),
                           ('ip=”1.1.1.1″', '搜索IP为 ”1.1.1.1”的资产'),
                           ('ip=”220.181.111.1/24″', '搜索起始IP为”220.181.111.1“的C段资产'),
                           ('ip.port_count>”2″', '搜索开放端口大于2的IP（支持等于、大于、小于）'),
                           ('app=”Hikvision 海康威视 Firmware 5.0+” && ip.ports=”8000″', '检索使用了Hikvision且ip开放8000端口的资产'),
                           ('ip.ports=”80″ && ip.ports=”443″', '查询开放了80和443端口号的资产'),
                           ('ip.port=”6379″', '搜索开放端口为”6379“的资产'),
                           ('ip.isp=”电信”', '搜索运营商为”中国电信”的资产'),
                           ('ip.country=”CN” 或 ip.country=”中国”', '搜索IP对应主机所在国为”中国“的资产'),
                           ('ip.province=”江苏”', '搜索IP对应主机在江苏省的资产'), ('ip.city=”北京”', '搜索IP对应主机所在城市为”北京“市的资产'),
                           ('ip.os=”Windows”', '搜索操作系统标记为”Windows“的资产'), ('&&', '&&同and，表示和'), ('||', '||同or，表示或'),
                           ('=', '模糊查询，表示查询包含关键词的资产'), ('==', '精确查询，表示查询有且仅有关键词的资产'), ('!=', '模糊剔除，表示剔除包含关键词的资产'),
                           ('!==', '精确剔除，表示剔除有且仅有关键词的资产')]

    shodan_query_syntax = [('http.title:"系统"', '指定网站标题'), ('http.status:200', '指定返回响应码'),
                           ('http.server:Apache/2.4.7', '指定返回中的server类型'),
                           ('http.html:"hello world"', '指定网页内容'), ('http.favicon.hash', '指定网站图标hash'),
                           ('country:"CN"', '限定国家'),
                           ('city:"ShangHai"', '限定城市'), ('hostname:baidu.com', '限定主机名或域名'),
                           ('org:"alibaba"', '限定组织或机构'),
                           ('os:"Windows Server 2008 R2"', '限定系统OS版本'), ('port:22', '限定端口'),
                           ('net:"59.56.19.0/24"', '指定网段'),
                           ('product:"mysql"', '指定使用的软件或产品'), ('vuln:"CVE-2014-0723"', '指定CVE漏洞编号'),
                           ('geo:"31.25,121.44"', '指定地理位置'),
                           ('isp:"China Telecom"', '指定ISP供应商')]

    zoomeye_query_syntax = [('country:"CN"', '搜索国家地区资产'), ('搜索国家地区资产', '搜索相关指定行政区的资产'), ('city:"changsha"', '搜索相关城市资产'),
                            ('ssl:"google"', '搜索ssl证书存在"google"字符串的资产'), ('ssl.cert.availability:1', '搜索证书是否在有效期内'),
                            ('ssl.cert.fingerprint:"F3C98F223D82CC41CF83D94671CCC6C69873FABF"', '搜索证书相关指纹资产'),
                            ('ssl.chain_count:3', '搜索ssl链计数资产'), ('ssl.cert.alg:"SHA256-RSA"', '搜索证书支持的签名算法'),
                            ('ssl.cert.issuer.cn:"pbx.wildix.com"', '搜索用户证书签发者通用域名名称'),
                            ('ssl.cert.pubkey.rsa.bits:2048', '搜索rsa_bits证书公钥位数'),
                            ('ssl.cert.pubkey.ecdsa.bits:256', '搜索ecdsa_bits证书公钥位数'),
                            ('ssl.cert.pubkey.type:"RSA"', '搜索证书的公钥类型'),
                            ('ssl.cert.serial:"18460192207935675900910674501"', '搜索证书序列号'),
                            ('ssl.cipher.bits:"128"', '搜索加密套件位数'),
                            ('ssl.cipher.name:"TLS_AES_128_GCM_SHA256"', '搜索加密套件名称'),
                            ('ssl.cipher.version:"TLSv1.3"', '搜索加密套件版本'),
                            ('ssl.version:"TLSv1.3"', '搜索证书的ssl版本'),
                            ('ssl.cert.subject.cn:"baidu.com"', '搜索用户证书持有者通用域名名称'),
                            ('ip:"8.8.8.8"', '搜索指定IPv4地址相关资产'),
                            ('ip:"2600:3c00::f03c:91ff:fefc:574a"', '搜索指定IPv6地址相关资产'),
                            ('cidr:52.2.254.36/24', '搜索IP的C段资产'), ('org:"北京大学"', '搜索相关组织(Organization)的资产'),
                            ('isp:"ChinaMobile"', '搜索相关网络服务提供商的资产'),
                            ('asn:42893', '搜索对应ASN自治系统编号相关IP资产'),
                            ('port:80', '搜索相关端口资产'), ('hostname:google.com', '搜索相关IP"主机名"的资产'),
                            ('site:baidu.com', '搜索域名相关的资产'),
                            ('app:"Cisco ASA SSL VPN"', '搜索思科ASA-SSL-VPN的设备'), ('service:"ssh"', '搜索对应服务协议的资产'),
                            ('device:"router"', '搜索路由器相关的设备类型'), ('os:"RouterOS"', '搜索相关操作系统'),
                            ('title:"Cisco"', '搜索html内容里标题中存在"Cisco"的数据'), ('industry:"政府"', '搜索行业类型相关的资产'),
                            ('after:"2020-01-01" +port:"50050"', '搜索更新时间为"2020-01-01"端口为"50050"以后的资产'),
                            ('before:"2020-01-01" +port:"50050"', '搜索更新时间在"2020-01-01"端口为"50050"以前的资产'),
                            ('jarm:"29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"', '搜索相关jarm内容的资产'),
                            ('dig:"baidu.com 220.181.38.148"', '搜索相关dig内容的资产'),
                            ('iconhash:"f3418a443e7d841097c714d69ec4bc  b8"', '通过md5方式对目标数据进行解析，根据图标搜索相关内容的资产'),
                            ('iconhash:"1941681276"', '通过mmh3方式对目标数据进行解析，根据图标搜索相关内容的资产'),
                            ('filehash:"0b5ce08db7fb8fffe4e14d05588d49d9"', '通过上传方式进行查询，根据解析的文件数据搜索相关内容的资产'),
                            ('空格', '在搜索框中输入“空格”则表示“或”的运算逻辑'), ('+', '在搜索框中输入“+”则表示“且”的运算逻辑'),
                            ('-', '在搜索框中输入“-”则表示“非”的运算逻辑'),
                            ('()', '在搜索框中输入“()”则表示“优先处理”的运算逻辑')]

    quake_query_syntax = [('ip:"1.1.1.1"', 'IP地址及网段'), ('is_ipv6:"true"', '查询IPv6数据'),
                          ('is_latest :"true"', '查询最新的资产数据'),
                          ('port:"80"', '查询开放80端口的主机'), ('ports:"80,8080,8000"', '查询同时开放过80、8080、8000端口的主机'),
                          ('port:<80', '查询开放端口小于80的主机'), ('transport:"tcp"', '查询tcp数据'), ('asn:"12345"', '自治域号码'),
                          ('org:"No.31,Jin-rong Street"', '自治域归属组织名称'), ('hostname:"50-87-74-222.unifiedlayer.', '主机名'),
                          ('domain:"360.cn"', '网站域名'), ('os:"Windows"', '操作系统名称+版本'), ('service:"http"', '即应用协议名称'),
                          ('services:"rtsp,https,telnet"', '搜索某个主机同时支持的协议'), ('app:"Apache"', 'Apache服务器产品'),
                          ('version:"1.2.1"', '产品版本'), ('response:"奇虎科技"', '端口原生返回数据中包含"奇虎科技"的主机'),
                          ('cert:"奇虎科技"', '包含"奇虎科技"的证书'),
                          ('catalog:"IoT物联网"', '应用类别'), ('type:"防火墙"', '应用类型'), ('level:"硬件设备层"', '应用层级'),
                          ('vendor:"Sangfor深信服科技股份有限公司"', '应用生产厂商'), ('country:"China" country:"CN"', '国家（英文）与国家代码'),
                          ('country_cn:"中国"', '国家（中文）'), ('province:"Sichuan"', '省份（英文）'),
                          ('province_cn:"四川"', '省份（中文）'),
                          ('city:"Chengdu"', '城市（英文）'), ('city_cn:"成都"', '城市（中文）'), ('owner: "tencent.com"', 'IP归属单位'),
                          ('isp: "联通"', '运营商'), ('img_tag: "windows"', '图片标签'), ('img_ocr:"admin"', '图片OCR'),
                          ('sys_tag:"卫星互联网"', '系统标签'), ('status_code:200', 'http返回状态码'),
                          ('http_path:"/admin"', 'http请求路径'),
                          ('title:后台', '网页标题'), ('meta_keywords:"网络安全"', '网页关键字'),
                          ('server:Nginx', 'Web服务器名称（http headers里面的Server字段）'),
                          ('powered_by:PHP', '网站开发语言（http headers里面的X-Powered-By）'),
                          ('favicon:"0488faca4c19046b94d07c3ee83cf9d6"', '网页favicon的md5值'),
                          ('favicon.location', '网页favicon的url'),
                          ('host:"google.com"', '请求host的值'),
                          ('html_hash:"69d7683445fed9e517e33750615f46c0"', '网页html的md5值'),
                          ('headers:"ThinkPHP"', 'http headers字符串'),
                          ('header_order_hash:"42997ea42eb46037ecb1e514e8190b93"', 'HTTP头部所有key用英文逗号按序连接后取MD5'),
                          ('body:"奇虎"', '网页body内容'), ('security_text', '页面上取的一些信息，如邮箱、备案号等'),
                          ('robots_hash:"e4c3bfe695710c5610cf51723b3bdae2"', 'robots.txt的md5值'),
                          ('robots:"Discuz"', 'robots.txt的内容'),
                          ('sitemap_hash:10f3aa0c1bd43f07ef8ed178d8b97df1', 'sitemap.xml的md5值'),
                          ('sitemap:"archive"', 'sitemap.xml的内容'), ('icp:"京ICP备08010314号"', 'ICP备案号'),
                          ('copyright:" 360网络安全响应中心（360-CERT）"', '版权许可'), ('mail:"@163.com"', '邮箱地址'),
                          ('page_type:"登录页"', '页面类型'),
                          ('and', '且')]

    table = PrettyTable([qtype+'语法内容', qtype+'语法说明'])
    table.align = 'l'
    if qtype == 'fofa':
        for data in fofa_query_syntax:
            table.add_row([data[0], data[1]])
        print(table)
    elif qtype == 'shodan':
        for data in shodan_query_syntax:
            table.add_row([data[0], data[1]])
        print(table)
    elif qtype == 'hunter':
        for data in hunter_query_syntax:
            table.add_row([data[0], data[1]])
        print(table)
    elif qtype == 'zoomeye':
        for data in zoomeye_query_syntax:
            table.add_row([data[0], data[1]])
        print(table)
    elif qtype == 'quake':
        for data in quake_query_syntax:
            table.add_row([data[0], data[1]])
        print(table)
    else:
        print("搜索引擎类型输入错误！")
