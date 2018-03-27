%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name os_adminpass_python_novaclient_ext
%global pkg_name novaclient-ext-os-adminpass

Name:           python-%{pkg_name}
## Version:        0.1.0
Version:        0.1.1
## os_adminpass_python_novaclient_ext-0.1.0.tar.gz
Release:        2%{?dist}
Summary:        Mock object 3 framework

Group:          Development/Languages
License:        ASL 2.0
URL:            http://code.google.com/p/pymox
## https://github.com/naototty/conoha_boot_adminpass_python_novaclient_ext
Source0:        http://pypi.python.org/packages/source/m/mox/%{upstream_name}-%{version}.tar.gz
## https://github.com/naototty/conoha_boot_adminpass_python_novaclient_ext/archive/0.1.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
python-novaclient-ext-os-adminpass is a novaclient extension for OpenStack.

%prep
%setup -q -n %{upstream_name}-%{version}
# Fix non-executable-script error
# sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' mox.py
# sed -i '/^#!\/usr\/bin\/python2.4$/,+1 d' stubout.py
## [n-gohko@hp-pc-ip150 rpmbuild]$ grep -r adminPass ./os_adminpass_python_novaclient_ext-0.1.0
## ./os_adminpass_python_novaclient_ext-0.1.0/os_adminpass_python_novaclient_ext/__init__.py:API_ADMIN_PASS = "OS-DCF:adminPass"
## r 2
sed -i 's/OS-DCF:adminPass/adminPass/g' os_adminpass_python_novaclient_ext/__init__.py


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

#%%check
#%%{__python} mox3_test.py
#%%{__python} setup.py test --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)


%doc README.rst PKG-INFO debugfiles.list debuglinks.list debugsources.list elfbins.list setup.cfg
%{python_sitelib}/%{upstream_name}/*
#%%{python_sitelib}/%%{upstream_name}.py*
#%%{python_sitelib}/stubout.py*
%{python_sitelib}/%{upstream_name}-%{version}*.egg-info

%changelog
* Tue Mar 27 2018 Naoto Gohko <naoto-gohko@gmo.jp> - 0.1.1-1
- support novaclient v2 api

* Mon May 04 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 0.1.0-1
- Initial package

