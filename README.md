# da-transform-schemas
TRE follows an event-driven architecture software design pattern that is based on the concept of events,
where components or modules communicate with each other by sending and receiving messages when specific
events occur. Components are loosely coupled and communicate through messages, rather than direct method
calls or API invocations. When an event occurs, a message is sent to the messaging system, which then
delivers it to the appropriate component or components. Components can subscribe to specific types of
messages, and the messaging system ensures that each message is delivered to all interested subscribers.  

All messages used in TRE infrastructure must conform to a message schema defined in [tre_schemas/avro](https://github.com/nationalarchives/da-transform-schemas/tree/main/tre_schemas/avro) . The message schema defines the data elements, their types, and the order in which they appear in the message.

Using schema provide/allow:  
- Interoperability: Message schemas enable different components to communicate with each other, even if they are implemented using different technologies or programming languages. By adhering to a common message schema, components can ensure that the data they send and receive is understood by all other components in the system.
- Validation: Message schemas enable messages to be validated for correctness before they are processed by the system. This can prevent errors and inconsistencies caused by incompatible data formats or missing fields.
- Versioning: Message schemas can be versioned to support changes in the system. When a new version of the schema is introduced, older versions can still be used to process messages that conform to the older schema. This can help ensure backward compatibility and smooth upgrades.
- Documentation: Message schemas provide a clear and concise way to document the data elements and their meaning. This can help developers understand the messages they are sending and receiving, and ensure that they are using the correct data types and formats.  

### Schemas for the messages used within Transformation Engine infrastructure
The message schema are defined using [Avro format](https://avro.apache.org/) and messages written in JSON  
All messages follow the same structure.  
- properties: defined in [tre-event-properties.avsc](https://github.com/nationalarchives/da-transform-schemas/blob/main/tre_schemas/avro/tre-event-properties.avsc)
- parameters: message specific values that will allow processing of the event 

An example message schema [request-judgment-parse.avsc](https://github.com/nationalarchives/da-transform-schemas/blob/main/tre_schemas/avro/request-judgment-parse.avsc)  
Will produce a sample JSON message [request-judgment-parse.json](https://github.com/nationalarchives/da-transform-schemas/blob/main/json-examples-new-schema/request-judgment-parse.json)


```
{
  "properties" : {
    "messageType" : "uk.gov.nationalarchives.tre.messages.judgment.parse.RequestJudgmentParse",
    "timestamp" : "2023-03-29T11:00:12.280Z",
    "function" : "fcl-judgment-parse-request",
    "producer" : "FCL",
    "executionId" : "executionId344",
    "parentExecutionId" : null
  },
  "parameters" : {
    "judgmentURI" : "https://xxx.xxx.nationalarchives.gov.uk/abc/def/2022/2034/judgment.docx # or signed s3 link",
    "reference" : "FCL-12345 # should be treated as opaque string, ideally filename-ready",
    "originator": "FCL"
  }
}
```

## Code Generation
Scala classes are generated from the schema and released to maven central. To use in projects add the dependency to build.sbt  
```
libraryDependencies += "uk.gov.nationalarchives" % "da-transform-schemas" % "0.102"
```

The message can be encoded and decoded with circe generic, add to build.sbt
```
val circeVersion = "0.14.2"
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core",
  "io.circe" %% "circe-generic",
  "io.circe" %% "circe-parser",
  "io.circe" %% "circe-generic-extras"
).map(_ % circeVersion)
```

Implicit decoders and encoders must be provided for the Enumerations
```
import io.circe.generic.auto._
import io.circe.syntax._
import io.circe.{Decoder, Encoder}
import uk.gov.nationalarchives.tre.messages.event.Producer

  implicit val producerEncoder: Encoder[Producer.Value] = Encoder.encodeEnumeration(Producer)
  implicit val produceeDecoder: Decoder[Producer.Value] = Decoder.decodeEnumeration(Producer)
```








