# maDMP Evaluation Plugin

*Plugin to evaluate machine-actionable Data Management Plans (maDMPs) through integration with DMP Evaluation Service.*

Plugin UUID: `8d372e4a-6145-4863-9831-82eb0ead1195`

## How to Install

See the [Plugins](https://guide.ds-wizard.org/en/latest/more/self-hosted-dsw/configuration/plugins.html) page in the DSW Guide for instructions on how to install the plugin.

## Development

To run the [DMP Evaluation Service](https://github.com/OSTrails/DMP-Evaluation-Service) locally (on port 8090), start it with Docker Compose and start the plugin service:

```bash
docker compose up -d
cd service
make dev
```

Then set **DMP Evaluation Service URL** to `http://localhost:8090` in the plugin settings.

The `EVALUATION_SERVICE_API_URL` environment variable only sets the fallback for requests without a URL. The plugin always sends the URL from its settings, so the variable has no effect on requests from the plugin.

## Changelog

### 0.2.0

- Updated to changed API of DMP Evaluation Service (not versioned yet)
- Updated dependencies

### 0.1.0

Initial version of the prototype.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.
