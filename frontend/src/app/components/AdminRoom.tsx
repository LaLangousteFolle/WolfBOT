import RolesConfig from "../admin/RolesConfig";

export default function AdminRoom({ nbJoueurs }) {
  return (
    <>
      <h1>Settings</h1>
      <RolesConfig nbJoueurs={nbJoueurs} />
    </>
  );
}
