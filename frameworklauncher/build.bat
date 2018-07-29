@echo off

@rem Copyright (c) Microsoft Corporation
@rem All rights reserved.
@rem
@rem MIT License
@rem
@rem Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
@rem documentation files (the "Software"), to deal in the Software without restriction, including without limitation
@rem the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
@rem to permit persons to whom the Software is furnished to do so, subject to the following conditions:
@rem The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
@rem
@rem THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
@rem BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
@rem NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
@rem DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
@rem OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
@rem
@rem
@rem Copyright (c) Peking University 2018
@rem
@rem The software is released under the Open-Intelligence Open Source License V1.0.
@rem The copyright owner promises to follow "Open-Intelligence Open Source Platform
@rem Management Regulation V1.0", which is provided by The New Generation of 
@rem Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).

@rem Start a new cmd.exe to avoid exit the caller cmd.exe.
cmd /c "%~dp0build-internal.bat" %*