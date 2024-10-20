Summary: Rotates, compresses, removes and mails system log files
Name: logrotate
Version: 3.18.0
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Base
Source: https://github.com/logrotate/logrotate/releases/download/%{version}/logrotate-%{version}.tar.gz
Requires: coreutils >= 5.92 libsepol libselinux popt
BuildRequires: libselinux-devel popt-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{!?_licensedir:%global license %%doc}

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%setup -q

%build
%configure \
  --with-selinux
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib

install -p -m 644 examples/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.conf
install -p -m 644 examples/btmp $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/btmp
install -p -m 644 examples/wtmp $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/wtmp
install -p -m 755 examples/logrotate.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/logrotate
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/logrotate.status

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license COPYING
%attr(0755, root, root) %{_sbindir}/logrotate
%attr(0644, root, root) %{_mandir}/man8/logrotate.8*
%attr(0644, root, root) %{_mandir}/man5/logrotate.conf.5*
%attr(0755, root, root) %{_sysconfdir}/cron.daily/logrotate
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/logrotate.conf
%attr(0755, root, root) %{_sysconfdir}/logrotate.d
%attr(0644, root, root) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/logrotate.status
