import sbt.url
import sbtrelease.ReleasePlugin.autoImport.ReleaseTransformations._

name := "da-transform-schema"
organization := "uk.gov.nationalarchives"

scmInfo := Some(
  ScmInfo(
    url("https://github.com/nationalarchives/da-transform-schema"),
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

releaseIgnoreUntrackedFiles := true
useGpgPinentry := true
publishTo := sonatypePublishToBundle.value
publishMavenStyle := true

releaseProcess := Seq[ReleaseStep](
  checkSnapshotDependencies, // check that there are no SNAPSHOT dependencies
  inquireVersions, // ask user to enter the current and next verion
  runClean, // clean
  runTest, // run tests
  setReleaseVersion, // set release version in version.sbt
  commitReleaseVersion, // commit the release version
  tagRelease, // create git tag
  releaseStepCommandAndRemaining("+publishSigned"), // run +publishSigned command to sonatype stage release
  setNextVersion, // set next version in version.sbt
  commitNextVersion, // commit next version
  releaseStepCommand("sonatypeRelease"), // run sonatypeRelease and publish to maven central
  pushChanges // push changes to git
)

description := "Classes to be used by TRE Message producers/consunmers"
licenses := List("MIT" -> new URL("https://choosealicense.com/licenses/mit/"))
homepage := Some(url("https://github.com/nationalarchives/tdr-generated-grapqhl"))


version := "0.1"
scalaVersion := "2.13.8"

Compile / sourceGenerators += (Compile / avroScalaGenerate).taskValue
(Compile / avroScalaSource) := new java.io.File(s"${baseDirectory.value}/src/main")
(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/tre_schemas/avro")








