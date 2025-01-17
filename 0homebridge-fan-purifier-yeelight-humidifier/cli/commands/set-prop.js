const log = require('../log');
const chalk = require('chalk');
const MiioProtocolHelper = require('../../lib/tools/MiioProtocolHelper');
const MiotProtocolUtils = require('../../lib/utils/MiotProtocolUtils');

exports.command = 'set-prop <ip> <propId> <value>';
exports.description = 'Set the value for the specified property id';
exports.builder = {
  token: {
    required: false,
    alias: 't',
    type: 'string',
    description: 'The device token'
  },
  retries: {
    required: false,
    alias: 'r',
    type: 'number',
    description: 'Number of retries'
  },
  timeout: {
    required: false,
    alias: 'T',
    type: 'number',
    description: 'Timeout'
  },
  debug: {
    required: false,
    alias: 'd',
    type: 'boolean',
    description: 'Enable debug output'
  }
};

exports.handler = async argv => {
  const {
    ip,
    propId,
    value,
    token,
    retries,
    timeout,
    debug
  } = argv;

  let storedToken = MiioProtocolHelper.getStoredToken(ip);

  if (!storedToken && !token) {
    log.error(`No stored token for the device ${chalk.yellow(ip)} found! Please store a token or use the --token argument!`);
    process.exit(0);
  }

  let propIdStr = String(propId); // make sure we have a string

  if (!MiotProtocolUtils.isSpecId(propIdStr)) {
    log.error(`The specified property id is incorrect!`);
    process.exit(0);
  }

  if (!value) {
    log.error(`Missing value!`);
    process.exit(0);
  }

  let tokenToUse = token || storedToken;

  const propRequest = {};
  propRequest.siid = parseInt(propIdStr.split('.')[0]);
  propRequest.piid = parseInt(propIdStr.split('.')[1]);
  propRequest.value = value;

  const requestParams = [];
  requestParams.push(propRequest);

  try {
    log.info(`Connecting to device at  ${chalk.yellow(ip)}`);
    await MiioProtocolHelper.connect(ip, tokenToUse);
    log.info(`Device found! Setting property value: ${chalk.cyan.bold(propId)} to ${chalk.blueBright.bold(value)}`);
    const res = await MiioProtocolHelper.send(ip, "set_properties", requestParams, retries, timeout, debug);
    log.success(`Successfully set property value!`);
  } catch (err) {
    log.error(err.message);
  }

  process.exit(0);
};
