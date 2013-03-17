# TODO
# - initscript
# - daemon user
# - logrotate
Summary:	logstash is a tool for managing events and logs
Name:		logstash
Version:	1.1.9
Release:	0.2
License:	Apache v2.0
Group:		Daemons
Source0:	http://logstash.objects.dreamhost.com/release/%{name}-%{version}-monolithic.jar
# Source0-md5:	70addd3ccd37e796f473fe5647c31126
URL:		http://www.logstash.net/
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
logstash is a tool for managing events and logs. You can use it to
collect logs, parse them, and store them for later use (like, for
searching). Speaking of searching, logstash comes with a web interface
for searching and drilling into all of your logs.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/patterns,%{_datadir}/%{name},/var/{lib,log}/logstash}
cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/%{name}/logstash-monolithic.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,logstash,logstash) %{_sysconfdir}/%{name}
%dir %attr(750,logstash,logstash) %{_sysconfdir}/%{name}/patterns
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}-monolithic.jar
%dir %attr(750,logstash,logstash) /var/lib/%{name}
%dir %attr(750,logstash,logstash) /var/log/%{name}
