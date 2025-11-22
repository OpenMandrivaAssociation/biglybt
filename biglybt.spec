# Prior to building on ABF
# Run `abb build` locally without the `tar zxf` line from prep or the --offline flag from build and comment out a file to break the build
# Archive the resulting vendor folder within the build directories and name it as seen with Source1
# Remove comments and test build with --offline again

%global debug_package %{nil}
%define uname BiglyBT
%define snap  3.4.0.1-SNAPSHOT
%define arch %(uname -m)

Name:       biglybt
Version:    3.9.0.0
Release:    1
Summary:    Feature-filled Bittorrent client based on the Azureus open source project
URL:        https://github.com/BiglySoftware/BiglyBT
Source0:    https://github.com/BiglySoftware/BiglyBT/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}-vendor.tar.gz
License:    GPL 2.0
Group:      Networking/File transfer

BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: javapackages-tools
BuildRequires: maven

%description
Source for BiglyBT, a feature filled, open source, ad-free, bittorrent client. BiglyBT is forked from the original project and is being maintained by two of the original developers as well as members of the community. With over 20 years of development, there's a good chance we have the features you are looking for.

%prep
%autosetup -p1 -n %{uname}-%{version}
# Must run without tar zxf line to generate Source1 archive
tar zxf %{S:1}

%build
export  JAVA_HOME='/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.302.%{arch}/'
export  PATH=$JAVA_HOME/bin:$PATH
# Must run without offline flag to generate Source1 archive
mvn clean package -DskipTests -Dmaven.repo.local=vendor/ --offline

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/java/%{name}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

cp core/target/%{name}-core-%{snap}.jar %{buildroot}%{_datadir}/java/%{name}/%{name}-core.jar
cp uis/target/%{uname}.jar %{buildroot}%{_datadir}/java/%{name}/%{name}.jar
cp uis/target/original-%{uname}.jar %{buildroot}%{_datadir}/java/%{name}/original-%{name}.jar
cp core/lib/commons-cli.jar %{buildroot}%{_datadir}/java/%{name}/commons-cli.jar
cp uis/lib/*linux*.jar %{buildroot}%{_datadir}/java/%{name}/

cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
exec java -cp "/usr/share/java/%{name}/*" com.%{name}.ui.Main "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}
rm -f %{_builddir}/%{uname}-%{version}/debugsourcefiles.list
chmod -R a+rX %{buildroot}

install -m 644 assets/linux/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -m 644 assets/linux/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -m 644 assets/linux/%{name}-lightgray.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}-lightgray.svg
install -m 644 assets/linux/%{name}.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%files
%{_datadir}/java/%{name}/original-%{name}.jar
%{_datadir}/java/%{name}/%{name}-core.jar
%{_datadir}/java/%{name}/%{name}.jar
%{_datadir}/java/%{name}/commons-cli.jar
%{_datadir}/java/%{name}/*linux*.jar
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/*.svg
