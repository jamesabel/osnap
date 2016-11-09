
# todo: to add packages from requirements file, just do a -r requirements
# todo: since everything we do now is using pip, just have a pip routine (not add_package() )


class OsnapyBase():
    def __init__(
            self,
            python_version,
            application_name    = None,
            clean_cache         = False,
            force_uninstalls    = False,
            architecture        = '64bit',
        ):
        self.architecture       = architecture
        self.application_name   = application_name
        self.clean_cache        = clean_cache
        self.force_uninstalls   = force_uninstalls
        self.python_version     = python_version

    def pip(self, package):
        raise NotImplementedError

    def create_python(self):
        "Create a full, stand-alone python installation with the required packages"
        raise NotImplementedError  # derived class provides this

    def add_package(self, package):
        raise NotImplementedError  # derived class provides this

