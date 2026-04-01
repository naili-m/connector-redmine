# Cert Manager
## About the connector
Basic Redmine API Client

## Version information

Connector Version: 1.0.0

Authored By: Naili.M

Certified: No

## Installing the connector
---------------------------------------------------------------

All connectors provided by FortiSOAR™ are delivered using a FortiSOAR™ repository. Therefore, you must set up your FortiSOAR™ repository and use the `yum` command to install connectors:

`yum install redmine-connector`

For the detailed procedure to install a connector, click[ here.](https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector)

## Configuring the connector
-----------------------------------------------------------------

- Server URL: The URL of the Redmine server, for example, `https://redmine.example.com`
- API Access Key: The API access key for authentication. You can generate an API access key
- SSL Verification: Enable or disable SSL verification for the Redmine server. By default, SSL verification is enabled.

### Actions supported by the connector
-----------------------------------------------------------------------------------

| Function | Description |
|-----|-----|
Run API Call|Run any API call supported by Redmine. You can specify the HTTP method, endpoint, and request body to interact with the Redmine API.|

Included playbooks
---------------------------------------------------

Each action has a sample playbook so you can quickly test it.