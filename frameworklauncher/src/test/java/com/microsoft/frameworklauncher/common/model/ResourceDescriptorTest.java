// Copyright (c) Microsoft Corporation
// All rights reserved. 
//
// MIT License
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
// documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
// the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
// to permit persons to whom the Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
// BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
//
//
// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).

package com.microsoft.frameworklauncher.common.model;

import com.microsoft.frameworklauncher.common.log.DefaultLogger;
import com.microsoft.frameworklauncher.common.utils.ValueRangeUtils;
import com.microsoft.frameworklauncher.common.utils.YamlUtils;
import com.microsoft.frameworklauncher.common.web.WebCommon;
import org.junit.Assert;
import org.junit.Test;


public class ResourceDescriptorTest {
  private static final DefaultLogger LOGGER = new DefaultLogger(ResourceDescriptorTest.class);

  @Test
  public void testResourceDescriptor() throws Exception {

    String resourceDescriptorJsonContent = "{\n" +
        "          \"cpuNumber\": 1,\n" +
        "          \"memoryMB\": 2,\n" +
        "          \"gpuNumber\": 3,\n" +
        "          \"portDefinitions\": {\n" +
        "          \t\"httpPort\": {\n" +
        "          \t\t\"start\": 0,\n" +
        "          \t\t\"count\": 1\n" +
        "          \t},\n" +
        "          \t\"sshPort\": {\n" +
        "          \t\t\"start\": 0,\n" +
        "          \t\t\"count\": 1\n" +
        "          \t}\n" +
        "          }\n" +
        "        }";
    String resourceDescriptorYamlContent = "!!com.microsoft.frameworklauncher.common.model.ResourceDescriptor\n" +
        "cpuNumber: 1\n" +
        "diskMB: 0\n" +
        "diskType: HDD\n" +
        "gpuAttribute: 0\n" +
        "gpuNumber: 3\n" +
        "memoryMB: 2\n" +
        "portDefinitions:\n" +
        "  httpPort: {count: 1, start: 0}\n" +
        "  sshPort: {count: 1, start: 0}\n";

    ResourceDescriptor resourceDescriptor = WebCommon.toObject(resourceDescriptorJsonContent, ResourceDescriptor.class);

    Assert.assertEquals(resourceDescriptor.getCpuNumber().intValue(), 1);
    Assert.assertEquals(resourceDescriptor.getGpuNumber().longValue(), 3L);
    Assert.assertEquals(resourceDescriptor.getPortNumber().intValue(), 2);

    ResourceDescriptor resourceDescriptor2 = YamlUtils.toObject(resourceDescriptorYamlContent.getBytes(), ResourceDescriptor.class);
    Assert.assertEquals(resourceDescriptor.getCpuNumber(), resourceDescriptor2.getCpuNumber());
    Assert.assertEquals(resourceDescriptor.getGpuNumber(), resourceDescriptor2.getGpuNumber());
    Assert.assertEquals(resourceDescriptor.getDiskMB(), resourceDescriptor2.getDiskMB());
    Assert.assertEquals(resourceDescriptor.getDiskType(), resourceDescriptor2.getDiskType());
    Assert.assertEquals(resourceDescriptor.getGpuAttribute(), resourceDescriptor2.getGpuAttribute());
    Assert.assertEquals(resourceDescriptor.getMemoryMB(), resourceDescriptor2.getMemoryMB());
    Assert.assertEquals(resourceDescriptor.getPortNumber(), resourceDescriptor2.getPortNumber());
    Assert.assertTrue(ValueRangeUtils.isEqualRangeList(resourceDescriptor.getPortRanges(), resourceDescriptor2.getPortRanges()));
  }
}

