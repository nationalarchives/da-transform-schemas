# 1. Messages to Find Case Law

Date: 2023-03-01

## Status

Very Draft

## Context

Find Case Law (FCL) would like to be able to send messages to the Transformation Engine (TRE)
to request parsing of judgments (either ones previously sent by Transfer Digital Records (TDR) or
novel ones), and TRE to respond with a parsed judgment and associated metadata from the TRE processes.

TRE would like to have proper schemas for the information that flows between TRE and FCL, and not
store/receive irrelevant information.

## Decision

There is a new format for the messages sent via SQS/SNS -- see commit "Discussed changes to the proposed messages"

Whilst AVRO is being used to define the schema, the actual messages are likely to be JSON.

When FCL would like a judgment in DOCX format parsing, it will send a link to a DOCX file
(which will probably be a signed S3 link, but this should be below the abstraction layer)
along with an opaque reference identifier controlled by FCL which will be sent back.
No other metadata (for example, FCLs record of the original submitter of the record to TDR) will be sent,
as TRE does not want to have to handle it. The identifier will be passed back by TRE to FCL,
and will also note the originator of the file was Find Case Law.

The [schema](../../tre_schemas/avro/fcl-judgment-parse-request.avsc) and [example json](../../json-examples/fcl-judgment-parse-request.json)
for this look good.

In response to either this request or a new judgment from a clerk submitted to TDR, a message will be
sent [schema](../../tre_schemas/avro/tre-judgment-available.avsc), [example json](../../json-examples/tre-judgment-available.json).

The response will continue to point to a tar.gz file with metadata in the previous format; however, FCL MUST support
the TDR section of the metadata.json being absent for documents that don't come from FCL.

TRE will maintain original format messages more or less indefinately.

## Consequences

???
