import sbt.url
import sbtrelease.ReleasePlugin.autoImport.ReleaseTransformations._

ThisBuild / name := "da-transform-schema"
ThisBuild / organization := "io.github.ian-hoyle"

// For all Sonatype accounts created on or after February 2021
ThisBuild / sonatypeCredentialHost := "s01.oss.sonatype.org"
sonatypeCredentialHost := "s01.oss.sonatype.org"
sonatypeRepository := "https://s01.oss.sonatype.org/service/local"

scmInfo := Some(
  ScmInfo(
    url("https://github.com/nationalarchives/da-transform-schema"),
    "git@github.com:nationalarchives/da-transform-schema.git"
  )
)

// disable publish with scala version, otherwise artifact name will include scala version
crossPaths := false

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
releaseVcsSign := true

releaseProcess := Seq[ReleaseStep](
  //checkSnapshotDependencies, // check that there are no SNAPSHOT dependencies
  inquireVersions, // ask user to enter the current and next version
  runClean, // clean
  runTest, // run tests
  setReleaseVersion, // set release version in version.sbt
  commitReleaseVersion, // commit the release version
  //tagRelease, // create git tag
  //releaseStepCommand("publishSigned"),
  //releaseStepCommand("sonatypeBundleRelease"),
  setNextVersion, // set next version in version.sbt
  commitNextVersion, // commit next version
  pushChanges // push changes to git
)

description := "Classes to be used by TRE Message producers/consumers"
licenses := List("MIT" -> new URL("https://choosealicense.com/licenses/mit/"))
homepage := Some(url("https://github.com/nationalarchives/da-transform-schema"))


scalaVersion := "2.13.10"

Compile / sourceGenerators += (Compile / avroScalaGenerate).taskValue
(Compile / avroScalaSource) := new java.io.File(s"${baseDirectory.value}/src/main")
(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/tre_schemas/avro")








