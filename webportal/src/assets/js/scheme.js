// Copyright (c) Peking University 2018
//
// The software is released under the Open-Intelligence Open Source License V1.0.
// The copyright owner promises to follow "Open-Intelligence Open Source Platform
// Management Regulation V1.0", which is provided by The New Generation of 
// Artificial Intelligence Technology Innovation Strategic Alliance (the AITISA).


const portTypeSchema =
  {
  type: "object",
  headerTemplate: "{{ self.label }}",
  options: {
    disable_edit_json: true,
  },
  properties: {
    label: {
      type: "string",
      description: "Label name for the port type",
    },
    beginAt: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: false,
      description: "The port to begin with in the port type, 0 for random selection",
    },
    portNumber: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: false,
      description: "Number of ports for the specific type",
    },
  },
  required: [
    "label",
    "beginAt",
    "portNumber",
  ],
};

const taskRoleSchema = {
  type: "object",
  headerTemplate: "{{ self.name }}",
  format: "grid",
  options: {
    disable_edit_json: true,
  },
  properties: {
    name: {
      type: "string",
      pattern: "^[A-Za-z0-9._~]+$",
      description: "Name for the task role, need to be unique with other roles",
    },
    taskNumber: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: true,
      description: "Number of tasks for the task role, no less than 1",
    },
    cpuNumber: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: true,
      description: "CPU number for one task in the task role, no less than 1",
    },
    memoryMB: {
      type: "number",
      multipleOf: 1,
      minimum: 100,
      exclusiveMinimum: false,
      description: "Memory for one task in the task role, no less than 100",
    },
    gpuNumber: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: false,
      description: "GPU number for one task in the task role, no less than 0",
    },
    command: {
      type: "string",
      pattern: "\\S+",
      format: "textarea",
      propertyOrder: 1001,
      options: {
        // expand_height: true,
      },
      description: "Executable command for tasks in the task role, can not be empty",
    },
    portList: {
      type: "array",
      format: "table",
      items: portTypeSchema,
      propertyOrder: 1002,
      description: "List of portType to use",
    },
  },
  required: [
    "name",
    "taskNumber",
    "cpuNumber",
    "memoryMB",
    "gpuNumber",
    "command",
  ],
}

const jobSchema = {
  type: "object",
  format: "grid",
  title: "Submit Form",
  properties: {
    jobName: {
      type: "string",
      pattern: "^[A-Za-z0-9\-._~]+$",
      propertyOrder: 100,
      options: {
        grid_columns: 4,
      },
      description: "Name for the job, need to be unique",
    },
    image: {
      type: "string",
      pattern: "\\S+",
      propertyOrder: 110,
      options: {
        grid_columns: 4,
      },
      exclusiveMinimum: true,
      description: "URL pointing to the Docker image for all tasks in the job",
    },
    authFile: {
      type: "string",
      propertyOrder: 120,
      options: {
        grid_columns: 4,
      },
      description: "Docker registry authentication file existing on HDFS",
      default: "",
    },
    dataDir: {
      type: "string",
      propertyOrder: 130,
      options: {
        grid_columns: 4,
      },
      description: "Data directory existing on HDFS",
      default: "",
    },
    outputDir: {
      type: "string",
      propertyOrder: 140,
      options: {
        grid_columns: 4,
      },
      description: "Output directory on HDFS, $PAI_DEFAULT_FS_URI/Output/$jobName will be used if not specified",
      default: "",
    },
    codeDir: {
      type: "string",
      propertyOrder: 150,
      options: {
        grid_columns: 4,
      },
      description: "Code directory existing on HDFS",
      default: "",
    },
    virtualCluster: {
      type: "string",
      propertyOrder: 125,
      options: {
        grid_columns: 3,
      },
      description: "The virtual cluster job runs on. If omitted, the job will run on default virtual cluster",
      default: "default",
    },
    gpuType: {
      type: "string",
      propertyOrder: 126,
      options: {
        grid_columns: 3,
      },
      description: "If omitted, the job will run on any gpu type",
      default: "",
    },
    killAllOnCompletedTaskNumber: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: true,
      propertyOrder: 127,
      options: {
        grid_columns: 3,
      },
      description: "Number of completed tasks to kill the entire job, no less than 0",
      default: 1,
    },
    retryCount: {
      type: "number",
      multipleOf: 1,
      minimum: 0,
      exclusiveMinimum: false,
      propertyOrder: 128,
      options: {
        grid_columns: 3,
      },
      description: "List of taskRole, one task role at least",
      default: 0,
    },
    taskRoles: {
      type: "array",
      items: taskRoleSchema,
      minItems: 1,
      format: "tabs",
      propertyOrder: 1000,
      description: "List of taskRole, one task role at least",
    },
  },
  required: [
    "jobName",
    "image",
    "taskRoles",
  ],
};

module.exports = jobSchema;
