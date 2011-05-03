%define _requires_exceptions make

Name:		puppet-dashboard
Version:	1.1.0
Release:	%mkrel 1
Summary:	Puppet web interface 
License:	GPL or Artistic
Group:		Development/Perl
Url:		http://www.puppetlabs.com/puppet/related-projects/dashboard/
Source0:	http://puppetlabs.com/downloads/dashboard/puppet-dashboard-%{version}.tar.gz
Source1:    %{name}.init
Requires:   ruby-mysql
Requires:   ruby-rake
Requires:   ruby-RubyGems
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The Puppet Dashboard is a web interface and reporting tool for your Puppet
installation. Dashboard facilitates management and configuration tasks,
provides a quick visual snapshot of important system information, and delivers
valuable reports. In the future, it will also serve to integrate with other IT
tools commonly used alongside Puppet.

%prep
%setup -q
find . -name .gitignore | xargs rm -f

%build


%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr app %{buildroot}%{_datadir}/%{name}
cp -pr bin %{buildroot}%{_datadir}/%{name}
cp -pr config %{buildroot}%{_datadir}/%{name}
cp -pr db %{buildroot}%{_datadir}/%{name}
cp -pr ext %{buildroot}%{_datadir}/%{name}
cp -pr lib %{buildroot}%{_datadir}/%{name}
cp -pr script %{buildroot}%{_datadir}/%{name}
cp -pr spec %{buildroot}%{_datadir}/%{name}
cp -pr vendor %{buildroot}%{_datadir}/%{name}
install -m 644 Rakefile %{buildroot}%{_datadir}/%{name}
install -m 644 VERSION %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_datadir}/%{name}/config/database.yml.example \
    %{buildroot}%{_sysconfdir}/%{name}.conf
chmod 640 %{buildroot}%{_sysconfdir}/%{name}.conf
pushd %{buildroot}%{_datadir}/%{name}/config
ln -s ../../../..%{_sysconfdir}/%{name}.conf database.yml
popd

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/tmp
cp -pr public %{buildroot}%{_localstatedir}/lib/%{name}

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_localstatedir}/log/%{name} log
ln -s ../../..%{_localstatedir}/lib/%{name}/tmp tmp
ln -s ../../..%{_localstatedir}/lib/%{name}/public public
popd

pushd %{buildroot}%{_localstatedir}/lib/%{name}/tmp
ln -s ../../run/%{name} pids
popd

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd dashboard %{_localstatedir}/lib/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING LICENSE README.markdown README_PACKAGES.markdown
%doc RELEASE_NOTES.md
%{_datadir}/%{name}
%{_initrddir}/%{name}
%attr(-,dashboard,dashboard) %{_localstatedir}/log/%{name}
%attr(-,dashboard,dashboard) %{_localstatedir}/lib/%{name}
%attr(-,dashboard,dashboard) %{_localstatedir}/run/%{name}
%attr(-,root,dashboard) %config(noreplace) %{_sysconfdir}/%{name}.conf

