# 1. Messages to Find Case Law

Date: 2023-03-01

## Status

Very Draft

## Context

Find Case Law (FCL) would like to be able to send messages to the Transformation Engine (TRE)
to request parsing of judgments (either ones previously sent by Transfer Digital Records (TDR) or
novel ones), and TRE to respond with a parsed judgment and associated metadata from the TRE processes.

TRE would like to have proper schemas for the information that flows between TRE and FCL, and emphasise
that TRE is not a document store. ???

???

## Decision

When FCL would like a judgment in DOCX format parsing, it will send a link to a DOCX file
(which will probably be a signed S3 link, but this should be below the abstraction layer)
along with an opaque reference identifier controlled by FCL which will be sent back.
No other metadata (for example, FCLs record of the original submitter of the record to TDR) will be sent,
as TRE does not want to have to handle it. The identifier will be passed back by TRE to FCL.

The [schema](../../tre_schemas/avro/fcl-judgment-parse-request.avsc) and [example json](../../json-examples/fcl-judgment-parse-request.json)
for this look good.

(Where and how do we send these messages? Error cases?)

In response to either this request or a new judgment from a clerk submitted to TDR, a message will be
sent [schema](../../tre_schemas/avro/tre-judgment-available.avsc), [example json](../../json-examples/tre-judgment-available.json).

??? TODO: TDR metadata, PARSER metadata, TRE metadata,

Currently the schema doesn't handle the array data the parser can emit.

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated.
