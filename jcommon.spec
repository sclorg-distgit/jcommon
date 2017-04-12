%{?scl:%scl_package jcommon}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%if 0%{?rhel}

%if 0%{?rhel} <= 6
  # EL 6
  %global custom_release 60
%else
  # EL 7
  %global custom_release 70
%endif

%else

%global custom_release 1

%endif

Name: %{?scl_prefix}jcommon
Version: 1.0.18
Release: %{custom_release}.3%{?dist}
Summary: JFree Java utility classes
License: LGPLv2+
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreechart/%{pkg_name}-%{version}.tar.gz
Source2: bnd.properties
URL: http://www.jfree.org/jcommon
BuildRequires:  %{?scl_prefix_maven}javapackages-local
BuildRequires:  %{?scl_prefix_java-common}ant
# Required for converting jars to OSGi bundles
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
BuildArch: noarch

%description
JCommon is a collection of useful classes used by 
JFreeChart, JFreeReport and other projects.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
%{?scl:Requires: %scl_runtime}

%description javadoc
Javadoc for %{name}.

%package xml
Summary: JFree XML utility classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description xml
Optional XML utility classes.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
find . -name "*.jar" -exec rm -f {} \;
%mvn_file org.jfree:%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
pushd ant
ant compile compile-xml javadoc
popd
# Convert to OSGi bundle
java -Djcommon.bundle.version="%{version}" \
     -jar $(build-classpath aqute-bnd) wrap -output %{pkg_name}-%{version}.bar -properties %{SOURCE2} %{pkg_name}-%{version}.jar
mv %{pkg_name}-%{version}.bar %{pkg_name}-%{version}.jar
%mvn_artifact pom.xml %{pkg_name}-%{version}.jar
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install -J javadoc
cp -p %{pkg_name}-xml-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}-xml.jar
%{?scl:EOF}

%files -f .mfiles
%doc licence-LGPL.txt README.txt

%files xml
%{_javadir}/%{pkg_name}-xml.jar

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Jan 17 2017 Jie Kang <jkang@redhat.com> 1.0.18-3
- Rebuild for RHSCL 2.4

* Fri Jun 24 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-2
- Change BR to rh-maven33-javapackages-local.

* Wed Jun 22 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-1
- Rebuild for rh-thermostat16.
