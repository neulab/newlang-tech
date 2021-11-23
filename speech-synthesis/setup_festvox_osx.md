# Setting up Festvox on OSX

When setting up Festvox on OSX, you may encounter an error either while running festvox_build.sh or when running your first commands. 

The error we address here comes from `path-to/speech_tools/include/EST_math.h`.
The following fix worked for my version of 0SX and is worth a try.

**Steps**
1. Change the definitions for OSX. 

Open and inspect the file:
```
vim path-to/speech_tools/EST_math.h
```

The block of interest is :

```
/* Apple OSX */
#if defined(__APPLE__)
#define isnanf(X) isnan((double)(X))
/* on some previous versions of OSX we seemed to need the following */
/* but not on 10.4 */
/* #define isnan(X) __isnan(X) */
#endif
```
Change it to : 

```
/* Apple OSX */
#if defined(__APPLE__)
#define isnanf(X) isnan((double)(X))
#define finite(X) isfinite((double)(X))
/* on some previous versions of OSX we seemed to need the following */
/* but not on 10.4 */
/* #define isnan(X) __isnan(X) */
#endif
```
2. Recompile the tools.

```
cd path-to/speech_tools
./configure
make
make test
make install

cd path-to/festival
./configure
make
make install

cd path-to/festvox
./configure
make
```
3. Test that your installation is correct.

Move to the festival directory and run festvox in interavtive mode:
```
cd path-to/festival
bin/festival
```
Then run:
```
festival> (SayText "hello world")
festival> (intro)
```
If the installation was successful and your audio setup is correct, you will hear "hello world" from the first command and two short sentences from the second command.

Exit festival:
```
festival> (quit)

```
Finally, test that it works in script mode. While still in the festival directory,  run:
```
examples/saytime
```
If you hear your local time read out, your installation was successful.



Let us know if you encounter other errors by raising an issue.




