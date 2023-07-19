import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.must.Matchers
import uk.gov.nationalarchives.da.messages.bag.available.BagAvailable

class CaseClassToJsonSchema extends AnyFlatSpec with Matchers {

    import com.github.andyglow.jsonschema.AsCirce._
    import json._
    import json.schema.Version._

    "Scala convertor" should "Turn Scala BagAvailable case class to JsonSchema containing COURT_DOCUMENT" in  {
       val fooSchema = Json.schema[BagAvailable].asCirce(Draft04())
       println(fooSchema)
       assert(fooSchema.toString() contains ("COURT_DOCUMENT"))
    }
}
