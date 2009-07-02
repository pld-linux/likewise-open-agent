#
%define concurrentdir   /usr/lib/likewise
%define man_dir         %{_mandir}
%define lw_bin_dir      /usr/share/likewise/bin
%define lw_perlpm_dir   %{lw_bin_dir}/Centeris
%define lw_agent_dir    /usr/share/likewise/open-agent
%define lw_client_dir   /usr/share/likewise/open-agent/client
%define lw_agent_bin_dir %{lw_agent_dir}/bin
%define lw_data_dir      /usr/share/centeris/data
%define lw_client_files  %(find ../Windows/Install/LikewiseOpen/bin/?elease/* -type f -printf '/usr/share/likewise/open-agent/client/%f\\n')

Summary:	Likewise Open Agent - Linux authentication on a Microsoft network using AD
Name:		likewise-open-agent
Version:	0.12.1
Release:	0.1
License:	CDDL v1.0
Group:		Applications
Source0:	http://www.mirrorservice.org/sites/download.sourceforge.net/pub/sourceforge/l/li/likewiseopenagt/%{name}-%{version}-src.tar.gz
# Source0-md5:	4136d0d29d8aab09509033f8211a554c
URL:		http://www.likewisesoftware.com/
BuildRequires:	ant
BuildRequires:	autoconf
BuildRequires:	concurrent
BuildRequires:	jpackage-utils
BuildRequires:	heimdal-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	samba-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-Convert-ASN1 >= 0.18
Requires:	perl-SOAP-Lite >= 0.66
Requires:	perl-URI
Requires:	perl-URI >= 1.33
Requires:	perl-XML-Parser >= 2.34
Requires:	perl-libwww-perl
Requires:	samba >= 3.0.20
Requires:	samba-client >= 3.0.20
Requires:	samba-winbind >= 3.0.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Likewise Open Agent provides Microsoft Windows system administrators
an easy way to perform basic administration of Linux servers for file
and print using the familiar Microsoft Management Console(MMC)
tools/wizards built into Windows.

Likewise Open Agent works in conjunction with Samba, CUPS and other
Linux applications. Many management functions utilize Samba and its
RPC mechanisms and callouts. Functionality not supported by Microsoft
RPC and Samba is provided through SOAP services calls to a server
hosted using SOAP-Lite.

Supports using the Windows Microsoft Management Console (MMC) to
perform the following administration task on Linux(R) servers:
- Add/delete/modify file shares
- Add/delete/modify print shares
- Use the Device Manager plug-in to view the properties of a Linux
  system
- Right-click on a Linux server to view properties and/or shut down
  the machine
- Collect events from the Linux system for display through the
  Microsoft Event Viewer
- Using Samba 3.0.21 or later, provide performance counter
  information through the perfmon client application



%prep
%setup -q
sed -i -e 's/^concurrentdir/#concurentdir/' Linux/cesm-agent/build.properties

%build
cd Linux
%ant build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{lw_bin_dir},%{lw_perlpm_dir},%{lw_agent_dir}/log}
install -d $RPM_BUILD_ROOT{%{lw_agent_bin_dir},%{lw_data_dir}/{likewise-open,windows/system32}}
install -d $RPM_BUILD_ROOT{%{lw_client_dir},%{man_dir}/man7,/etc/rc.d/init.d}

cd Linux
install EventLogDB/EventLogs.pm $RPM_BUILD_ROOT%{lw_perlpm_dir}
install EventLogDB/evtsyslog.pl $RPM_BUILD_ROOT%{lw_bin_dir}
install EventLogDB/dist/likewisemsg.dll $RPM_BUILD_ROOT%{lw_data_dir}/windows/system32/likewisemsg.dll
install EventLogDB/likewise-evtlogd $RPM_BUILD_ROOT%{lw_bin_dir}
install HWInfoFilter/hwinfo_filter.pl $RPM_BUILD_ROOT%{lw_bin_dir}
install SambaScripts/shutdown $RPM_BUILD_ROOT%{lw_bin_dir}
install SambaScripts/abort_shutdown $RPM_BUILD_ROOT%{lw_bin_dir}
if [ -e ../Windows/Install/LikewiseOpen/bin/?elease/ ]; then
   install ../Windows/Install/LikewiseOpen/bin/?elease/* $RPM_BUILD_ROOT%{lw_client_dir}
fi
install ./VERSION $RPM_BUILD_ROOT%{lw_agent_bin_dir}/VERSION
install cesm-agent/dist/likewise-open-agent.pl $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/SambaCommands.jar $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/sambaPrint $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/sambaShare $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/sambaShareInstaller $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/likewise-open $RPM_BUILD_ROOT/etc/rc.d/init.d
install cesm-agent/dist/likewise-open $RPM_BUILD_ROOT%{lw_bin_dir}
install cesm-agent/dist/findjre.sh $RPM_BUILD_ROOT%{lw_agent_bin_dir}
install cesm-agent/dist/postinstall.sh $RPM_BUILD_ROOT%{lw_bin_dir}
install cesm-agent/dist/likewise-perfd $RPM_BUILD_ROOT%{lw_bin_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
