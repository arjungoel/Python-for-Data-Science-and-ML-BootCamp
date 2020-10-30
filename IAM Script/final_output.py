import pandas as pd


class OutputContextManager:

    def __init__(self, iam_role_report, iam_user_report, user_group_report):
        self.iam_role_report = pd.read_csv("iam_role_policies.csv")
        self.iam_user_report = pd.read_csv("iam_user_policies.csv")
        self.user_group_report = pd.read_csv("list_groups_user.csv")

    def __enter__(self):
        self.iam_output = pd.merge(self.iam_role_report, self.iam_user_report,
                                   left_index=True, right_index=True, how='outer')
        self.final_output = pd.merge(
            self.iam_output, self.user_group_report, left_index=True, right_index=True, how='outer')
        return self.final_output

    def __exit__(self, *exec):
        print(f"Exit: {self.final_output}")


with OutputContextManager("RoleReport", "UserReport", "UserInGroupReport") as final_output:
    print(final_output)
