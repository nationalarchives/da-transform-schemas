name := "da-transform-schema"
organization := "uk.gov.tna.dri.tre"


version := "0.1"
scalaVersion := "2.13.8"

Compile / sourceGenerators += (Compile / avroScalaGenerate).taskValue
//Test / sourceGenerators += (Test / avroScalaGenerate).taskValue
//
(Compile / avroScalaSource) := new java.io.File(s"${baseDirectory.value}/src/main")
//(Test / avroScalaSource) := new java.io.File(s"${baseDirectory.value}/mytestoutputdir")
//
(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/tre_schemas/avro")
//(Compile / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/src/main/myavro2")
//
//(Test / avroSourceDirectories) += new java.io.File(s"${baseDirectory.value}/src/test/avro2")
//
//(Compile / avroScalaCustomNamespace) := Map("example"->"overridden", "example2"->"overridden2")
//
//Compile / avroScalaCustomTypes := {
//  avrohugger.format.Standard.defaultTypes.copy(
//    array = avrohugger.types.ScalaVector,
//    union = avrohugger.types.OptionalShapelessCoproduct)
//}
//
//
//libraryDependencies ++= Seq(
//  "com.chuusai" %% "shapeless" % "2.3.2",
//  "org.apache.avro" % "avro" % "1.7.7"
//)









