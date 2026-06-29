# AWS `mxgraph.aws4` resIcon names — verified vs blank

draw.io's AWS shape set uses `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<NAME>`.
The `<NAME>` values are **inconsistent** — many obvious guesses render as an empty
coloured tile. The canonical aliases live in `assets/aws_icons.py` (`AWS4`); this
doc records the gotchas and how to extend safely. All "verified" names below were
rendered and visually confirmed in draw.io desktop 30.x.

## The traps (verified BLANK — do NOT use → use the RIGHT name)

| You'd guess (BLANK) | Correct name (RENDERS) | Service |
|---|---|---|
| `simple_storage_service` | `s3` | S3 |
| `sagemaker_ai` | `sagemaker` | SageMaker |
| `amazon_bedrock` | `bedrock` | Bedrock |
| `opensearch_service`, `amazon_opensearch_service` | `elasticsearch_service` | OpenSearch |
| `data_firehose` | `kinesis_data_firehose` | Firehose |
| `iam_identity_center`, `identity_center`, `aws_iam_identity_center` | `identity_and_access_management` (or `single_sign_on`) | IAM / SSO |
| `elastic_kubernetes_service` | `eks` | EKS |
| `managed_streaming_for_apache_kafka` | (no resourceIcon — use `mq` or emoji) | MSK/Kafka |
| `public_subnet`, `private_subnet`, `vpc_router` | (no resourceIcon — use `route_table` / a caption) | subnets |
| `documentdb`, `simple_queue_service`, `managed_grafana`, `marketplace`, `devices`, `peering_connection` | (blank — find an alternative + verify) | misc |

## Verified RENDERS (by category — these are the `AWS4` values)
- **storage:** `s3`
- **analytics:** `glue`, `athena`, `lake_formation`, `kinesis_data_streams`, `kinesis_data_firehose`, `quicksight`, `elasticsearch_service`, `emr`, `glue_databrew`
- **security/identity:** `key_management_service`, `macie`, `secrets_manager`, `identity_and_access_management`, `single_sign_on`, `shield`, `detective`, `guardduty`, `security_lake`, `network_access_control_list`
- **ml/ai:** `sagemaker`, `bedrock`, `comprehend`, `kendra`, `q`, `rekognition`, `augmented_ai`
- **compute:** `lambda`, `ec2`, `eks`, `traditional_server`
- **app integration:** `step_functions`, `eventbridge`, `api_gateway`, `mq`, `application_integration`
- **management:** `systems_manager`, `cloudwatch`, `cloudtrail`, `config`, `xray`
- **networking:** `transit_gateway`, `direct_connect`, `virtual_private_cloud`, `internet_gateway`, `nat_gateway`, `elastic_load_balancing_application_load_balancer`, `site_to_site_vpn`, `router`, `route_table`, `endpoints`, `elastic_network_interface`
- **databases:** `rds`, `aurora`, `dynamodb`
- **generic:** `users`, `user`, `corporate_data_center`

## Adding a new icon (always verify)
1. `python3 assets/verify_icons.py <candidate1> <candidate2> ...` (raw resIcon names).
2. Open `/tmp/icontest.png`. A glyph = it renders; a flat coloured square = it does NOT — try another name.
3. Add the working name to `AWS4` in `assets/aws_icons.py` as `"alias": ("name", "category")`.

## Non-AWS concepts → emoji (render in colour on macOS/PowerPoint)
SaaS `☁️`, Web/Mobile `📱`, Logs `📜`, Metrics `📈`, personas `👔 🛠️ 🎧 🛡️ 💰 📊`,
value icons `🔒 🔑 📜 ⚙ 📈 💲 🛡 ⭐`, pipeline steps `🔀 ✨ 🔒 ⛔ 🔗 🧬 📦`.
Pass an emoji where the builder expects an icon alias (`ic_tb`, `bv`, `pcard`) and
it's rendered as centred text instead of an AWS tile.
