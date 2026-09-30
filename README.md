# maDMP Evaluation Plugin

*Plugin to evaluate machine-actionable Data Management Plans (maDMPs) through integration with DMP Evaluation Service.*

Plugin UUID: `8d372e4a-6145-4863-9831-82eb0ead1195`

## How to Install

See the [Plugins](https://guide.ds-wizard.org/en/latest/more/self-hosted-dsw/configuration/plugins.html) page in the DSW Guide for instructions on how to install the plugin.

## Development

To run the [DMP Evaluation Service](https://github.com/OSTrails/DMP-Evaluation-Service) locally (on port 8090), start it with Docker Compose and point the plugin service to it:

```bash
docker compose up -d
cd service
EVALUATION_SERVICE_API_URL=http://localhost:8090 make dev
```

## Changelog

### 0.2.0

- Updated to changed API of DMP Evaluation Service (not versioned yet)
- Updated dependencies

### 0.1.0

Initial version of the prototype.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.
