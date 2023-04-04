import sbt.url
import ReleaseTransformations._
import java.io.FileWriter

name := "da-transform-schema"
organization := "uk.gov.nationalarchives"

ThisBuild / organization := "uk.gov.nationalarchives"
ThisBuild / organizationName := "National Archives"

lazy val setLatestTagOutput = taskKey[Unit]("Sets a GitHub actions output for the latest tag")

setLatestTagOutput := {
  val fileWriter = new FileWriter(sys.env("GITHUB_OUTPUT"), true)
  fileWriter.write(s"latest-tag=${(ThisBuild / version).value}\n")
  fileWriter.close()
}

scmInfo := Some(
  ScmInfo(
    url("https://github.com/nationalarchives/tdr-generated-graphql"),
    "git@github.com:nationalarchives/da-transform-schema.git"
  )
)

developers := List(
  Developer(
    id    = "tna-digital-archiving-jenkins",
    name  = "TNA Digital Archiving",
    email = "digitalpreservation@nationalarchives.gov.uk",
    url   = url("https://github.com/nationalarchives/da-transform-schema")
  )
)

useGpgPinentry := true
publishTo := sonatypePublishToBundle.value
publishMavenStyle := true

releaseProcess := Seq[ReleaseStep](
  checkSnapshotDependencies,
  inquireVersions,
  runClean,
  runTest,
  setReleaseVersion,
  releaseStepTask(setLatestTagOutput),
  commitReleaseVersion,
  tagRelease,
  releaseStepCommand("publishSigned"),
  releaseStepCommand("sonatypeBundleRelease"),
  setNextVersion,
  commitNextVersion,
  pushChanges
)

description := "Classes to be used by TRE Message producers/consunmers"
licenses := List("MIT" -> new URL("https://choosealicense.com/licenses/mit/"))
homepage := Some(url("https://github.com/nationalarchives/tdr-generated-grapqhl"))


version := "0.1"
scalaVersion := "2.13.8"

Compile / sourceGenerators += (Compile / avroScalaGenerate).taskValue
(Compile / avroScalaSource) := new java.io.File(s"${baseDirectory.value}/src/main")
(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/tre_schemas/avro")








