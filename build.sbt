import sbt.url
import sbtrelease.ReleasePlugin.autoImport.ReleaseTransformations._

ThisBuild / name := "da-transform-schema"
ThisBuild / organization := "uk.gov.nationalarchives"

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
    id    = "tna-da-bot",
    name  = "TNA Digital Archiving",
    email = "s-GitHubDABot@nationalarchives.gov.uk",
    url   = url("https://github.com/nationalarchives/da-transform-schema")
  )
)

releaseIgnoreUntrackedFiles := true
useGpgPinentry := true
publishTo := {
  val centralSnapshots = "https://central.sonatype.com/repository/maven-snapshots/"
  if (isSnapshot.value) Some("central-snapshots" at centralSnapshots)
  else localStaging.value
}
publishMavenStyle := true

releaseProcess := Seq[ReleaseStep](
  checkSnapshotDependencies, // check that there are no SNAPSHOT dependencies
  inquireVersions, // ask user to enter the current and next version
  runClean, // clean
  runTest, // run tests
  setReleaseVersion, // set release version in version.sbt
  commitReleaseVersion, // commit the release version
  tagRelease, // create git tag
  releaseStepCommand("publishSigned"),
  releaseStepCommand("sonaRelease"),
  setNextVersion, // set next version in version.sbt
  commitNextVersion, // commit next version
  pushChanges // push changes to git
)

description := "Classes to be used by TRE Message producers/consumers"
licenses := List("MIT" -> new URL("https://choosealicense.com/licenses/mit/"))
homepage := Some(url("https://github.com/nationalarchives/da-transform-schema"))


libraryDependencies += "com.github.andyglow" %% "scala-jsonschema" % "0.7.11"
libraryDependencies ++= Seq(
  "com.github.andyglow" %% "scala-jsonschema-core" %  "0.7.11",
  "com.github.andyglow" %% "scala-jsonschema-circe-json" %  "0.7.11"
)
libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.19" % Test

scalaVersion := "2.13.18"

Compile / sourceGenerators += (Compile / avroScalaGenerate).taskValue
(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/tre_schemas/avro")
