# Autotrolej Data Source

## Overview

Rijeka Transit uses the public Autotrolej API as its primary source of public
transport data for Rijeka, Croatia.

Swagger documentation:

`https://api.autotrolej.hr/api/open/swagger/index.html`

The API provides access to:

- bus stops
- transit lines
- scheduled departures
- current vehicle positions
- authentication and token refresh

All communication with the Autotrolej API will eventually be handled by the
Rijeka Transit backend. The frontend should not communicate with the
Autotrolej API directly.

---

## Authentication

### Login

Endpoint:

`GET /api/open/v1/token/login`

Headers:

| Header | Type |
|---|---|
| `Username` | string |
| `Password` | string |

A successful request returns an authentication token as plain text.

Credentials and authentication tokens must never be stored in the repository
or exposed to the frontend.

### Token refresh

Endpoint:

`GET /api/open/v1/token/refresh`

Headers:

| Header | Type |
|---|---|
| `Username` | string |
| `token` | string |

A successful request returns a refreshed token as plain text.

The exact token lifetime has not yet been determined.

---

## Vehicle positions

### Get all vehicles

Endpoint:

`GET /api/open/v1/voznired/autobusi`

Header:

`token`

Example vehicle:

```json
{
  "gbr": 820,
  "lon": 14.438259,
  "lat": 45.327831,
  "voznjaId": 1433676,
  "voznjaBusId": 2209202
}
```

Observed fields:

| Field | Description |
|---|---|
| `gbr` | Vehicle identifier |
| `lon` | Current longitude |
| `lat` | Current latitude |
| `voznjaId` | Associated trip ID when available |
| `voznjaBusId` | Vehicle-trip related identifier |

`voznjaId` can be `null`.

During API exploration, some invalid coordinates (`0, 0`) and duplicate
vehicle records were observed. Rijeka Transit should therefore validate and
deduplicate vehicle data before exposing it to clients.

### Get individual vehicle

Endpoint:

`GET /api/open/v1/voznired/autobus`

Parameters:

| Parameter | Location | Type |
|---|---|---|
| `token` | header | string |
| `gbr` | query | integer |

The response uses the same vehicle structure as the `/autobusi` endpoint but
allows a vehicle to be queried by its `gbr`.

---

## Bus stops

### Get stops

Endpoint:

`GET /api/open/v1/voznired/stanice`

Header:

`token`

Observed stop fields include:

| Field | Description |
|---|---|
| `id` | Stop ID |
| `naziv` | Stop name |
| `nazivKratki` | Short stop name |
| `gpsX` | Longitude |
| `gpsY` | Latitude |
| `smjer` | Direction |
| `smjerId` | Direction ID |
| `stanicaIdSuprotniSmjer` | ID of the stop serving the opposite direction |
| `polazakList` | Associated departure data |

The API uses `gpsX` for longitude and `gpsY` for latitude.

---

## Transit lines

### Get lines

Endpoint:

`GET /api/open/v1/voznired/linije`

Header:

`token`

Observed line fields include:

| Field | Description |
|---|---|
| `id` | Line ID |
| `brojLinije` | Public line number |
| `smjerId` | Direction ID |
| `smjerNaziv` | Direction name |
| `varijantaId` | Route variant ID |
| `naziv` | Line/route description |
| `polazakList` | Associated departure data |

The API also exposes a composite line identifier such as:

`2132-2-0`

This value is referred to by the API as `uniqueLinijaId`.

---

## Departures by stop

Endpoint:

`GET /api/open/v1/voznired/polasciStanica`

Parameters:

| Parameter | Location | Type |
|---|---|---|
| `token` | header | string |
| `stanicaId` | query | integer |

The endpoint returns information about the requested stop together with its
`polazakList`.

Observed departure fields:

| Field | Description |
|---|---|
| `stanicaId` | Stop ID |
| `voznjaId` | Trip ID |
| `voznjaBusId` | Vehicle-trip related identifier |
| `voznjaStanicaId` | Trip-stop related identifier |
| `linijaId` | Line ID |
| `uniqueLinijaId` | Composite line identifier |
| `polazak` | Scheduled departure timestamp |
| `dolazak` | Scheduled arrival timestamp |

The response may contain departures covering multiple dates rather than only
the next upcoming departure.

---

## Departures by line

Endpoint:

`GET /api/open/v1/voznired/polasciLinija`

Parameters:

| Parameter | Location | Type |
|---|---|---|
| `token` | header | string |
| `uniqueLinijaId` | query | string |

A successful request using a value such as `2132-2-0` returns line information
and its `polazakList`.

The returned line information includes the line number, direction, variant,
name, and scheduled departures.

---

## Relationships discovered

The API exposes several identifiers that may allow data from different
endpoints to be connected:

```text
Vehicle
  |
  | voznjaId
  v
Trip / Departure
  |
  +---- linijaId / uniqueLinijaId ----> Line
  |
  +---- stanicaId --------------------> Stop
```

In particular, some live vehicles contain a non-null `voznjaId`. Departure
records also contain `voznjaId`, providing a possible direct relationship
between live vehicle positions and scheduled trips.

This relationship will be investigated further during implementation.

---

## Known API considerations

Initial exploration identified several behaviours that the Rijeka Transit
backend should account for:

- `voznjaId` is not always available for live vehicles.
- Vehicle responses may contain duplicate records.
- Vehicle coordinates may contain invalid values such as `(0, 0)`.
- Some API requests return server errors when required parameters are missing.
- Authentication tokens should be managed only by the backend.
- The exact authentication token lifetime is currently unknown.

These behaviours mean the application should not simply forward raw
Autotrolej responses to the frontend. The backend will provide validation,
normalization and error handling around the upstream API.
