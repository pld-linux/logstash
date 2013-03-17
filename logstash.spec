# TODO
# - daemon user
Summary:	logstash is a tool for managing events and logs
Name:		logstash
Version:	1.1.9
Release:	0.4
License:	Apache v2.0
Group:		Daemons
Source0:	http://logstash.objects.dreamhost.com/release/%{name}-%{version}-monolithic.jar
# Source0-md5:	70addd3ccd37e796f473fe5647c31126
Source1:	%{name}-agent.init
Source2:	%{name}-agent.sysconfig
Source3:	%{name}-agent.conf
Source4:	%{name}.logrotate
URL:		http://www.logstash.net/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	jre
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	no_install_post_check_tmpfiles 1

%description
logstash is a tool for managing events and logs. You can use it to
collect logs, parse them, and store them for later use (like, for
searching). Speaking of searching, logstash comes with a web interface
for searching and drilling into all of your logs.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/patterns,/etc/{rc.d/init.d,sysconfig,logrotate.d}} \
	$RPM_BUILD_ROOT{%{_datadir}/%{name},/var/{lib,log,run}/logstash}
cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/%{name}/logstash-monolithic.jar
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/logstash-agent
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/logstash-agent
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/agent.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/logstash

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add logstash-agent
%service logstash-agent restart

%preun
if [ "$1" = "0" ]; then
	%service -q logstash-agent stop
	/sbin/chkconfig --del logstash-agent
fi

%files
%defattr(644,root,root,755)
%dir %attr(750,logstash,logstash) %{_sysconfdir}/%{name}
%dir %attr(750,logstash,logstash) %{_sysconfdir}/%{name}/patterns
%config(noreplace) %verify(not md5 mtime size) %attr(640,logstash,logstash)  %{_sysconfdir}/%{name}/agent.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) /etc/sysconfig/logstash-agent
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) /etc/logrotate.d/logstash
%attr(754,root,root) /etc/rc.d/init.d/logstash-agent
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}-monolithic.jar
%dir %attr(770,root,logstash) /var/lib/%{name}
%dir %attr(770,root,logstash) /var/log/%{name}
%dir %attr(770,root,logstash) /var/run/%{name}
