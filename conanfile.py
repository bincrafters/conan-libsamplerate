from conans import ConanFile, CMake, tools
import os


class LibSampleRateConan(ConanFile):
    name = "libsamplerate"
    version = "0.1.9"
    description = "Secret Rabbit Code (aka libsamplerate) is a Sample Rate Converter for audio"
    topics = ("conan", "libsamplerate", "audio", "resampler", "converter")
    url = "https://github.com/bincrafters/conan-libsamplerate"
    homepage = "http://www.mega-nerd.com/SRC/index.html"
    license = "BSD-2-Clause	"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    revision = "b12668ac1c0a223d0effd13447e7f7c3a6690912"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/erikd/libsamplerate/"
        tools.get("{0}/archive/{1}.zip".format(source_url, self.revision),
                  sha256="89ddb93785b27aa9ce12a8dbbee0be535e605afa852eda91556bb881e99c0cb4")
        extracted_dir = self.name + "-" + self.revision
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["LIBSAMPLERATE_TESTS"] = False
        cmake.definitions["LIBSAMPLERATE_INSTALL"] = True
        # these dependencies are needed only for tests
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_ALSA"] = True
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_Sndfile"] = True
        cmake.definitions["CMAKE_DISABLE_FIND_PACKAGE_FFTW"] = True
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                              "install(FILES ${CMAKE_BINARY_DIR}/samplerate.pc DESTINATION lib/pkgconfig)",
                              "install(FILES ${CMAKE_CURRENT_BINARY_DIR}/samplerate.pc DESTINATION lib/pkgconfig)")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.libs = ["libsamplerate-0.lib"]
            self.cpp_info.bindirs.append(os.path.join(self.package_folder, "lib"))
        else:
            self.cpp_info.libs = ["samplerate"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("winmm")
        elif self.settings.os == "Macos":
            frameworks = ['CoreAudio']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
