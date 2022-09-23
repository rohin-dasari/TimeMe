import setuptools

setuptools.setup(
        name="TimeMe",
        version="0.0.1",
        author="Rohin Dasari",
        author_email='rohin.dasari@gmail.com',
        description="A small package to help \
        time/profile the execution of functions \
        and manage experiments measuring run time",
        packages=['timeme'],
        python_requires='>=3.6',
        install_requires=[
                'pandas',
                'tqdm'
            ],
        license='MIT'
        )


