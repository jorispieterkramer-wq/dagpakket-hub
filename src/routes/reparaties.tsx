import { createFileRoute } from "@tanstack/react-router";
import { PageStub } from "@/components/dashboard/Page";

export const Route = createFileRoute("/reparaties")({ component: () => <PageStub title="Reparaties" description="Reparatie tickets per product: status open/in reparatie/gereed." /> });
