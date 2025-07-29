# UniFi Network API Documentation (Partial)

This document outlines the UniFi Network API endpoints and their expected request/response structures, based on current implementation and available documentation. This serves as a reference for the Gemini agent.

## Endpoints

### GET /v1/sites

Retrieves a paginated list of local sites managed by this Network application.

- **Description:** List Local Sites
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites`
- **Query Parameters:**
    - `offset` (number, optional): Start offset for pagination. Default: 0.
    - `limit` (number, optional): Maximum number of items to return. Default: 25, Max: 200.
    - `filter` (string, optional): Filter criteria (e.g., `name.eq('Default')`).
- **Response (200 OK):**
```json
{
  "offset": 0,
  "limit": 25,
  "count": 1,
  "totalCount": 1,
  "data": [
    {
      "id": "<site-uuid>",
      "internalReference": "<string>",
      "name": "<string>"
    }
  ]
}
```

### GET /v1/info

Retrieves general information about the UniFi Network application.

- **Description:** Get Application Info
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/info`
- **Response (200 OK):**
```json
{
  "applicationVersion": "<string>"
}
```

### GET /v1/sites/{siteId}/devices

Retrieves a paginated list of all adopted devices on a site.

- **Description:** List Devices
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/devices`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
- **Query Parameters:**
    - `offset` (number, optional): Start offset for pagination. Default: 0.
    - `limit` (number, optional): Maximum number of items to return. Default: 25, Max: 200.
    - `filter` (string, optional): Filter criteria (Note: Filterable properties not explicitly documented in provided API spec).
- **Response (200 OK):**
```json
{
  "offset": 0,
  "limit": 25,
  "count": 10,
  "totalCount": 1000,
  "data": [
    {
      "id": "<device-uuid>",
      "name": "<string>",
      "model": "<string>",
      "macAddress": "<string>",
      "ipAddress": "<string>",
      "state": "<string>",
      "features": [],
      "interfaces": []
    }
  ]
}
```

### GET /v1/sites/{siteId}/devices/{deviceId}

Retrieves detailed information about a specific adopted device.

- **Description:** Get Device Details
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `deviceId` (string, required): The UUID of the device.
- **Response (200 OK):**
```json
{
  "id": "<device-uuid>",
  "name": "<string>",
  "model": "<string>",
  "supported": <boolean>,
  "macAddress": "<string>",
  "ipAddress": "<string>",
  "state": "<string>",
  "firmwareVersion": "<string>",
  "firmwareUpdatable": <boolean>,
  "adoptedAt": "<timestamp>",
  "provisionedAt": "<timestamp>",
  "configurationId": "<string>",
  "uplink": {},
  "features": {},
  "interfaces": {}
}
```

### POST /v1/sites/{siteId}/devices/{deviceId}/actions

Performs an action on a specific adopted device.

- **Description:** Execute Device Action
- **Method:** POST
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}/actions`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `deviceId` (string, required): The UUID of the device.
- **Request Body (application/json):**
```json
{
  "action": "RESTART"  // Only RESTART is currently implemented
}
```
- **Response (200 OK):** (No specific response body documented, typically success)

### POST /v1/sites/{siteId}/devices/{deviceId}/interfaces/ports/{portIdx}/actions

Performs an action on a specific device port.

- **Description:** Execute Port Action
- **Method:** POST
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}/interfaces/ports/{portIdx}/actions`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `deviceId` (string, required): The UUID of the device.
    - `portIdx` (integer, required): The index of the port.
- **Request Body (application/json):**
```json
{
  "action": "POWER_CYCLE" // Only POWER_CYCLE is currently implemented
}
```
- **Response (200 OK):** (No specific response body documented, typically success)

### GET /v1/sites/{siteId}/devices/{deviceId}/statistics/latest

Retrieves the latest real-time statistics of a specific adopted device.

- **Description:** Get Latest Device Statistics
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}/statistics/latest`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `deviceId` (string, required): The UUID of the device.
- **Response (200 OK):**
```json
{
  "uptimeSec": <integer>,
  "lastHeartbeatAt": "<timestamp>",
  "nextHeartbeatAt": "<timestamp>",
  "loadAverage1Min": <number>,
  "loadAverage5Min": <number>,
  "loadAverage15Min": <number>,
  "cpuUtilizationPct": <number>,
  "memoryUtilizationPct": <number>,
  "uplink": {
    "txRateBps": <integer>,
    "rxRateBps": <integer>
  },
  "interfaces": {}
}
```

### GET /v1/sites/{siteId}/clients

Retrieves a paginated list of all connected clients on a site.

- **Description:** List Connected Clients
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/clients`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
- **Query Parameters:**
    - `offset` (number, optional): Start offset for pagination. Default: 0.
    - `limit` (number, optional): Maximum number of items to return. Default: 25, Max: 200.
    - `filter` (string, optional): Filter criteria (e.g., `type.eq('WIRED')`).
- **Response (200 OK):**
```json
{
  "offset": 0,
  "limit": 25,
  "count": 10,
  "totalCount": 1000,
  "data": [
    {
      "id": "<client-uuid>",
      "name": "<string>",
      "connectedAt": "<timestamp>",
      "ipAddress": "<string>",
      "access": {
        "type": "<string>"
      },
      "type": "<string>",
      "macAddress": "<string>",
      "uplinkDeviceId": "<device-uuid>"
    }
  ]
}
```

### GET /v1/sites/{siteId}/clients/{clientId}

Retrieves detailed information about a specific connected client.

- **Description:** Get Connected Client Details
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/clients/{clientId}`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `clientId` (string, required): The UUID of the client.
- **Response (200 OK):**
```json
{
  "id": "<client-uuid>",
  "name": "<string>",
  "connectedAt": "<timestamp>",
  "ipAddress": "<string>",
  "access": {
    "type": "<string>"
  },
  "type": "<string>",
  "macAddress": "<string>",
  "uplinkDeviceId": "<device-uuid>"
}
```

### POST /api/s/{site}/cmd/stamgr (Client Actions)

Performs various actions on client devices.

- **Description:** Client Actions (Block, Unblock, Authorize Guest, Unauthorize Guest, Reconnect, Forget)
- **Method:** POST
- **Path:** `/api/s/{siteId}/cmd/stamgr`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
- **Request Body (application/json):**
```json
{
  "cmd": "block-sta" | "unblock-sta" | "authorize-guest" | "unauthorize-guest" | "kick-sta" | "forget-sta",
  "mac": "<client-mac-address>",
  "minutes": <integer, optional>,
  "up": <integer, optional>,
  "down": <integer, optional>,
  "bytes": <integer, optional>,
  "ap_mac": "<string, optional>"
}
```
- **Response (200 OK):** (Typically success, specific response varies by command)

### GET /v1/sites/{siteId}/hotspot/vouchers

Retrieves a paginated list of Hotspot vouchers.

- **Description:** List Vouchers
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/hotspot/vouchers`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
- **Query Parameters:**
    - `offset` (number, optional): Start offset for pagination. Default: 0.
    - `limit` (number, optional): Maximum number of items to return. Default: 100, Max: 1000.
    - `filter` (string, optional): Filter criteria (e.g., `name.eq('test-voucher')`).
- **Response (200 OK):**
```json
{
  "offset": 0,
  "limit": 100,
  "count": 10,
  "totalCount": 1000,
  "data": [
    {
      "id": "<voucher-uuid>",
      "createdAt": "<timestamp>",
      "name": "<string>",
      "code": "<string>",
      "authorizedGuestLimit": <integer>,
      "authorizedGuestCount": <integer>,
      "activatedAt": "<timestamp>",
      "expiresAt": "<timestamp>",
      "expired": <boolean>,
      "timeLimitMinutes": <integer>,
      "dataUsageLimitMBytes": <integer>,
      "rxRateLimitKbps": <integer>,
      "txRateLimitKbps": <integer>
    }
  ]
}
```

### POST /v1/sites/{siteId}/hotspot/vouchers

Creates one or more Hotspot vouchers.

- **Description:** Generate Vouchers
- **Method:** POST
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/hotspot/vouchers`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
- **Request Body (application/json):**
```json
{
  "count": <integer, 1-1000>,
  "name": "<string>",
  "authorizedGuestLimit": <integer, optional>,
  "timeLimitMinutes": <integer>,
  "dataUsageLimitMBytes": <integer, optional>,
  "rxRateLimitKbps": <integer, optional>,
  "txRateLimitKbps": <integer, optional>
}
```
- **Response (201 Created):**
```json
{
  "vouchers": [
    {}
  ]
}
```

### DELETE /v1/sites/{siteId}/hotspot/vouchers/{voucherId}

Removes a specific Hotspot voucher.

- **Description:** Delete Voucher
- **Method:** DELETE
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/hotspot/vouchers/{voucherId}`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `voucherId` (string, required): The UUID of the voucher.
- **Response (200 OK):**
```json
{
  "vouchersDeleted": <integer>
}
```

### GET /v1/sites/{siteId}/hotspot/vouchers/{voucherId}

Retrieves details of a specific Hotspot voucher.

- **Description:** Get Voucher Details
- **Method:** GET
- **Path:** `/proxy/network/integration/v1/sites/{siteId}/hotspot/vouchers/{voucherId}`
- **Path Parameters:**
    - `siteId` (string, required): The UUID of the site.
    - `voucherId` (string, required): The UUID of the voucher.
- **Response (200 OK):**
```json
{
  "id": "<voucher-uuid>",
  "createdAt": "<timestamp>",
  "name": "<string>",
  "code": "<string>",
  "authorizedGuestLimit": <integer>,
  "authorizedGuestCount": <integer>,
  "activatedAt": "<timestamp>",
  "expiresAt": "<timestamp>",
  "expired": <boolean>,
  "timeLimitMinutes": <integer>,
  "dataUsageLimitMBytes": <integer>,
  "rxRateLimitKbps": <integer>,
  "txRateLimitKbps": <integer>
}
```
